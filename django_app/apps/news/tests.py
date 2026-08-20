import pytest
from django.urls import reverse
from apps.accounts.models import AdminUser
from apps.news.models import NewsItem


@pytest.mark.django_db
def test_news_item_creation_and_auto_slug():
    item = NewsItem.objects.create(
        title='Internal Smart Hackathon 2026',
        category=NewsItem.Category.HACKATHON,
        content='Students from 2nd and 3rd year can register teams of 4 members before March 15th.',
        is_pinned=True,
    )
    assert item.slug == 'internal-smart-hackathon-2026'
    assert item.is_pinned is True
    assert item.summary != ''
    assert str(item) == 'Internal Smart Hackathon 2026'


@pytest.mark.django_db
def test_admin_can_create_and_manage_news(client):
    admin = AdminUser.objects.create_user(
        email='admin@valliammai.ac.in',
        password='StrongPassword123!',
        role=AdminUser.Role.SUPERADMIN
    )
    client.force_login(admin)

    # 1. Access manage news
    response = client.get(reverse('news:manage'))
    assert response.status_code == 200

    # 2. Add news
    add_url = reverse('news:add')
    post_data = {
        'title': 'Placement Drive: Zoho Corporation',
        'category': 'placement',
        'summary': 'Zoho on-campus drive for CSE final year batch.',
        'content': 'Zoho is visiting on 25th March. Eligibility: CGPA 7.5+ with no standing arrears.',
        'is_pinned': True,
        'is_published': True,
    }
    response = client.post(add_url, post_data, follow=True)
    assert response.status_code == 200
    assert NewsItem.objects.filter(title='Placement Drive: Zoho Corporation').exists()

    item = NewsItem.objects.get(title='Placement Drive: Zoho Corporation')
    assert item.is_pinned is True

    # 3. Edit news
    edit_url = reverse('news:edit', kwargs={'pk': item.pk})
    response = client.post(edit_url, {
        'title': 'Placement Drive: Zoho Corporation (Updated)',
        'category': 'placement',
        'summary': item.summary,
        'content': item.content,
        'is_pinned': False,
        'is_published': True,
    }, follow=True)
    assert response.status_code == 200
    item.refresh_from_db()
    assert item.title == 'Placement Drive: Zoho Corporation (Updated)'
    assert item.is_pinned is False

    # 4. Toggle Pin
    toggle_url = reverse('news:toggle_pin', kwargs={'pk': item.pk})
    client.post(toggle_url, follow=True)
    item.refresh_from_db()
    assert item.is_pinned is True

    # 5. Delete news
    delete_url = reverse('news:delete', kwargs={'pk': item.pk})
    client.post(delete_url, follow=True)
    assert not NewsItem.objects.filter(pk=item.pk).exists()


@pytest.mark.django_db
def test_public_news_list_detail_and_json_feed(client):
    item1 = NewsItem.objects.create(
        title='End Semester Exam Schedule Released',
        category=NewsItem.Category.EXAM,
        content='Anna University Nov/Dec examination timetable published.',
        is_pinned=True,
        is_published=True,
    )
    item2 = NewsItem.objects.create(
        title='Draft Notice Internal Review',
        category=NewsItem.Category.CIRCULAR,
        content='This is a draft notice.',
        is_published=False,
    )

    # Public list
    response = client.get(reverse('public_news:list'))
    assert response.status_code == 200
    assert 'End Semester Exam Schedule Released' in response.content.decode()
    assert 'Draft Notice Internal Review' not in response.content.decode()

    # Public detail & views count increment
    detail_url = reverse('public_news:detail', kwargs={'slug': item1.slug})
    response = client.get(detail_url)
    assert response.status_code == 200
    item1.refresh_from_db()
    assert item1.views_count == 1

    # Public JSON feed
    feed_url = reverse('public_news:feed')
    response = client.get(feed_url)
    assert response.status_code == 200
    data = response.json()
    assert 'news' in data
    assert len(data['news']) == 1
    assert data['news'][0]['title'] == 'End Semester Exam Schedule Released'
    assert data['news'][0]['is_pinned'] is True


@pytest.mark.django_db
def test_vapid_public_key_api(client):
    response = client.get(reverse('public_news:vapid_key'))
    assert response.status_code == 200
    data = response.json()
    assert 'publicKey' in data
    assert len(data['publicKey']) > 20


@pytest.mark.django_db
def test_push_subscribe_and_unsubscribe_api(client):
    from apps.news.models import PushSubscription
    
    # 1. Subscribe new device
    sub_payload = {
        'endpoint': 'https://fcm.googleapis.com/fcm/send/test-token-12345',
        'keys': {
            'p256dh': 'test-p256dh-key',
            'auth': 'test-auth-secret'
        },
        'category_filter': 'all'
    }
    response = client.post(
        reverse('public_news:push_subscribe'),
        data=sub_payload,
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'subscribed'
    assert data['created'] is True
    assert PushSubscription.objects.filter(endpoint='https://fcm.googleapis.com/fcm/send/test-token-12345', is_active=True).exists()

    # 2. Re-subscribe existing device (idempotency)
    response = client.post(
        reverse('public_news:push_subscribe'),
        data=sub_payload,
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json()['created'] is False
    assert PushSubscription.objects.count() == 1

    # 3. Unsubscribe
    unsub_payload = {'endpoint': 'https://fcm.googleapis.com/fcm/send/test-token-12345'}
    response = client.post(
        reverse('public_news:push_unsubscribe'),
        data=unsub_payload,
        content_type='application/json'
    )
    assert response.status_code == 200
    sub = PushSubscription.objects.get(endpoint='https://fcm.googleapis.com/fcm/send/test-token-12345')
    assert sub.is_active is False


@pytest.mark.django_db
def test_send_news_push_notification_task(monkeypatch):
    from apps.news.models import NewsItem, PushSubscription
    from apps.news.tasks import send_news_push_notification

    news = NewsItem.objects.create(
        title='Urgent: Final Year Project Review Dates',
        category=NewsItem.Category.CIRCULAR,
        content='Project Phase 2 viva will commence from April 2nd in Computing Lab 3.',
        is_pinned=True,
        is_published=True
    )
    sub = PushSubscription.objects.create(
        endpoint='https://fcm.googleapis.com/fcm/send/student-device-token',
        p256dh='fake_p256dh',
        auth='fake_auth',
        is_active=True
    )

    webpush_calls = []
    def fake_webpush(subscription_info, data, vapid_private_key, vapid_claims, ttl):
        webpush_calls.append({
            'subscription_info': subscription_info,
            'data': data,
            'vapid_claims': vapid_claims
        })

    monkeypatch.setattr('apps.news.tasks.webpush', fake_webpush)

    result = send_news_push_notification(news.id)
    assert result['status'] == 'success'
    assert result['sent'] == 1
    assert len(webpush_calls) == 1

    # Verify payload content
    call_data = webpush_calls[0]['data']
    assert 'Urgent: Final Year Project Review Dates' in call_data
    assert news.slug in call_data

    # Verify model metrics updated
    news.refresh_from_db()
    assert news.push_count == 1
    assert news.last_pushed_at is not None


@pytest.mark.django_db
def test_admin_broadcast_push_view(client, monkeypatch):
    from apps.accounts.models import AdminUser
    from apps.news.models import NewsItem, PushSubscription

    admin = AdminUser.objects.create_user(
        email='hod.cse@valliammai.ac.in',
        password='StrongPassword123!',
        role=AdminUser.Role.SUPERADMIN
    )
    client.force_login(admin)

    news = NewsItem.objects.create(
        title='Infosys Campus Placement Results',
        category=NewsItem.Category.PLACEMENT,
        content='Congratulations to the 48 CSE students selected by Infosys!',
        is_published=True
    )
    PushSubscription.objects.create(
        endpoint='https://fcm.googleapis.com/fcm/send/phone-1',
        p256dh='k1',
        auth='a1',
        is_active=True
    )

    broadcast_task_called = []
    def fake_broadcast(news_id):
        broadcast_task_called.append(news_id)

    monkeypatch.setattr('apps.news.views.trigger_push_broadcast', fake_broadcast)

    url = reverse('news:broadcast_push', kwargs={'pk': news.pk})
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert len(broadcast_task_called) == 1
    assert broadcast_task_called[0] == news.id
