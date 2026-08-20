import json
import logging
from celery import shared_task
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from pywebpush import webpush, WebPushException
from .models import NewsItem, PushSubscription

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def send_news_push_notification(self, news_id):
    """
    Asynchronously broadcasts a web push notification to all subscribed student phones/browsers
    for a published news bulletin.
    """
    try:
        news = NewsItem.objects.get(id=news_id, is_published=True)
    except NewsItem.DoesNotExist:
        logger.warning("NewsItem %s not found or not published, skipping push notification.", news_id)
        return {'status': 'skipped', 'reason': 'News item not found or unpublished'}

    vapid_private_key = getattr(settings, 'VAPID_PRIVATE_KEY', '')
    vapid_admin_email = getattr(settings, 'VAPID_ADMIN_EMAIL', 'mailto:cse@valliammai.ac.in')

    if not vapid_private_key:
        logger.error("VAPID_PRIVATE_KEY is not configured in settings. Cannot send push notification.")
        return {'status': 'error', 'reason': 'Missing VAPID_PRIVATE_KEY'}

    category_badge = news.get_category_display()
    urgent_prefix = "🚨 [URGENT] " if news.is_pinned else "📢 "
    title = f"{urgent_prefix}[{category_badge}] {news.title}"
    if len(title) > 90:
        title = title[:87] + '...'

    body = news.summary or news.content
    # Clean up whitespace and truncate
    body = ' '.join(body.split())
    if len(body) > 160:
        body = body[:157] + '...'

    payload = json.dumps({
        'title': title,
        'body': body,
        'icon': '/static/images/brand-icon.png',
        'badge': '/static/images/badge-icon.png',
        'url': f"/news/{news.slug}/",
        'tag': f"cse-news-{news.id}",
        'requireInteraction': bool(news.is_pinned),
        'timestamp': int(timezone.now().timestamp() * 1000),
        'data': {
            'url': f"/news/{news.slug}/",
            'newsId': news.id,
            'category': news.category,
            'isPinned': news.is_pinned
        }
    })

    subscriptions = PushSubscription.objects.filter(is_active=True)
    sent_count = 0
    failed_count = 0
    deactivated_count = 0

    vapid_claims = {
        'sub': vapid_admin_email
    }

    for sub in subscriptions:
        # Category filter check: if student opted for a specific category
        if sub.category_filter and sub.category_filter != 'all' and sub.category_filter != news.category:
            continue

        subscription_info = {
            'endpoint': sub.endpoint,
            'keys': {
                'p256dh': sub.p256dh,
                'auth': sub.auth
            }
        }

        try:
            webpush(
                subscription_info=subscription_info,
                data=payload,
                vapid_private_key=vapid_private_key,
                vapid_claims=vapid_claims,
                ttl=86400  # 24 hours TTL
            )
            sent_count += 1
            PushSubscription.objects.filter(pk=sub.pk).update(last_notified_at=timezone.now())
        except WebPushException as exc:
            # Check response status code from push service (FCM / Mozilla / Apple)
            status_code = getattr(exc.response, 'status_code', None) if exc.response is not None else None
            if status_code in (404, 410):
                # Subscription has expired or user revoked browser permission
                PushSubscription.objects.filter(pk=sub.pk).update(is_active=False)
                deactivated_count += 1
                logger.info("Deactivated expired push subscription: %s (Status: %s)", sub.endpoint, status_code)
            else:
                failed_count += 1
                logger.warning("WebPush delivery failed for subscription %s: %s", sub.endpoint, exc)
        except Exception as exc:
            failed_count += 1
            logger.error("Unexpected error sending push to %s: %s", sub.endpoint, exc)

    # Update news metrics
    NewsItem.objects.filter(pk=news.pk).update(
        last_pushed_at=timezone.now(),
        push_count=F('push_count') + 1
    )

    logger.info(
        "Push notification completed for News #%s: %s sent, %s failed, %s deactivated.",
        news.id, sent_count, failed_count, deactivated_count
    )

    return {
        'status': 'success',
        'news_id': news.id,
        'sent': sent_count,
        'failed': failed_count,
        'deactivated': deactivated_count
    }
