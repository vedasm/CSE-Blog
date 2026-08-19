import datetime
import pytest
from django.urls import reverse
from apps.accounts.models import AdminUser
from apps.events.models import Event, ScheduleItem


@pytest.mark.django_db
def test_schedule_item_creation_and_properties():
    schedule = ScheduleItem.objects.create(
        title='Internal Assessment Test 1 (IAT-1)',
        category=ScheduleItem.Category.EXAM,
        start_date=datetime.date(2026, 8, 20),
        end_date=datetime.date(2026, 8, 25),
        start_time=datetime.time(9, 30),
        end_time=datetime.time(12, 30),
        venue='CSE Exam Halls 201-208',
        description='Covers Units 1 and 2 for all subjects.',
        is_academic_calendar=True,
    )
    assert schedule.is_multi_day is True
    assert schedule.category_color == '#EF4444'
    assert 'IAT-1' in str(schedule)


@pytest.mark.django_db
def test_event_auto_sync_to_schedule_and_no_duplicates():
    # 1. Create an Event (Hackathon)
    event = Event.objects.create(
        title='Smart India Hackathon 2026 Internal Round',
        category=Event.Category.HACKATHON,
        event_date=datetime.date(2026, 9, 15),
        event_time=datetime.time(10, 0),
        venue='CSE Advanced Computing Lab',
        description='Internal screening round for SIH 2026 ideas.',
        registration_link='https://hackathon.valliammai.ac.in',
    )

    # 2. Check that a ScheduleItem was automatically created via signal
    assert ScheduleItem.objects.filter(source_event=event).exists()
    schedule = ScheduleItem.objects.get(source_event=event)
    assert schedule.title == 'Smart India Hackathon 2026 Internal Round'
    assert schedule.category == ScheduleItem.Category.HACKATHON
    assert schedule.start_date == datetime.date(2026, 9, 15)
    assert schedule.venue == 'CSE Advanced Computing Lab'
    assert schedule.registration_link == 'https://hackathon.valliammai.ac.in'

    # 3. Modify the Event and verify ScheduleItem is updated (no duplicate created)
    event.title = 'Smart India Hackathon 2026 (Grand Finale)'
    event.event_date = datetime.date(2026, 9, 20)
    event.save()

    assert ScheduleItem.objects.filter(source_event=event).count() == 1
    schedule.refresh_from_db()
    assert schedule.title == 'Smart India Hackathon 2026 (Grand Finale)'
    assert schedule.start_date == datetime.date(2026, 9, 20)

    # 4. Delete the Event and verify ScheduleItem cascades cleanly
    event.delete()
    assert not ScheduleItem.objects.filter(title='Smart India Hackathon 2026 (Grand Finale)').exists()


@pytest.mark.django_db
def test_admin_can_manage_calendar_schedules(client):
    admin = AdminUser.objects.create_user(
        email='admin@valliammai.ac.in',
        password='StrongPassword123!',
        role=AdminUser.Role.SUPERADMIN
    )
    client.force_login(admin)

    # 1. Manage Schedules List View
    response = client.get(reverse('events:admin_schedules'))
    assert response.status_code == 200

    # 2. Add Academic Calendar Schedule
    add_url = reverse('events:add_schedule')
    post_data = {
        'title': 'Zoho On-Campus Placement Drive',
        'category': 'placement',
        'start_date': '2026-09-10',
        'end_date': '2026-09-11',
        'start_time': '09:00',
        'end_time': '17:00',
        'venue': 'CSE Placement Auditorium',
        'description': 'Online coding round and technical interviews for shortlisted 4th years.',
        'registration_link': 'https://placement.valliammai.ac.in/zoho',
        'is_academic_calendar': True,
        'is_published': True,
    }
    response = client.post(add_url, post_data, follow=True)
    assert response.status_code == 200
    assert ScheduleItem.objects.filter(title='Zoho On-Campus Placement Drive').exists()

    item = ScheduleItem.objects.get(title='Zoho On-Campus Placement Drive')
    assert item.category == 'placement'
    assert item.is_academic_calendar is True

    # 3. Edit Schedule
    edit_url = reverse('events:edit_schedule', kwargs={'pk': item.pk})
    response = client.post(edit_url, {
        'title': 'Zoho On-Campus Placement Drive (Day 1 & 2)',
        'category': 'placement',
        'start_date': '2026-09-10',
        'end_date': '2026-09-11',
        'start_time': '09:00',
        'venue': 'CSE Placement Auditorium',
        'description': item.description,
        'is_academic_calendar': True,
        'is_published': True,
    }, follow=True)
    assert response.status_code == 200
    item.refresh_from_db()
    assert item.title == 'Zoho On-Campus Placement Drive (Day 1 & 2)'

    # 4. Delete Schedule
    delete_url = reverse('events:delete_schedule', kwargs={'pk': item.pk})
    client.post(delete_url, follow=True)
    assert not ScheduleItem.objects.filter(pk=item.pk).exists()


@pytest.mark.django_db
def test_public_calendar_and_json_feed(client):
    item1 = ScheduleItem.objects.create(
        title='Model Practical Examination',
        category=ScheduleItem.Category.EXAM,
        start_date=datetime.date(2026, 8, 28),
        venue='Laboratory 3',
        is_published=True,
    )
    item2 = ScheduleItem.objects.create(
        title='Draft Schedule Not Published',
        category=ScheduleItem.Category.ACADEMIC,
        start_date=datetime.date(2026, 8, 30),
        is_published=False,
    )

    # 1. Public Calendar Page
    response = client.get(reverse('public_events:calendar'))
    assert response.status_code == 200
    assert 'Department &amp; Academic Calendar' in response.content.decode() or 'Department & Academic Calendar' in response.content.decode()

    # 2. Public JSON Feed
    feed_url = reverse('public_events:calendar_feed') + '?year=2026&month=8'
    response = client.get(feed_url)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert data['count'] == 1
    assert data['schedules'][0]['title'] == 'Model Practical Examination'
    assert data['schedules'][0]['category'] == 'exam'
    assert data['schedules'][0]['category_color'] == '#EF4444'
