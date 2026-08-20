from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class NewsItem(models.Model):
    class Category(models.TextChoices):
        ANNOUNCEMENT = 'announcement', 'General Announcement'
        CIRCULAR = 'circular', 'Official Circular'
        PLACEMENT = 'placement', 'Placement & Internship'
        EXAM = 'exam', 'Exam & Academics'
        HACKATHON = 'hackathon', 'Hackathon & Contest'
        EVENT = 'event', 'Event & Workshop'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.ANNOUNCEMENT
    )
    summary = models.TextField(
        max_length=500,
        blank=True,
        help_text='Brief preview summary shown on cards and feeds'
    )
    content = models.TextField(
        help_text='Detailed news content or circular description'
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name='Urgent / Pinned Bulletin',
        help_text='Highlight at top with pulse badge'
    )
    attachment = models.FileField(
        upload_to='news/attachments/%Y/%m/',
        blank=True,
        null=True,
        help_text='Optional PDF circular, document or image'
    )
    external_link = models.URLField(
        blank=True,
        help_text='Optional registration/external reference URL'
    )
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)
    last_pushed_at = models.DateTimeField(null=True, blank=True, help_text='Timestamp of the last web push broadcast')
    push_count = models.PositiveIntegerField(default=0, help_text='Number of times push broadcast was sent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-published_at', '-created_at']
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'news-item'
            unique_slug = base_slug
            num = 1
            while NewsItem.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        if not self.summary and self.content:
            # Auto-populate summary if empty
            plain = self.content.strip()
            self.summary = plain[:200] + ('...' if len(plain) > 200 else '')
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PushSubscription(models.Model):
    endpoint = models.URLField(max_length=500, unique=True, help_text='W3C Push Service endpoint URL')
    p256dh = models.CharField(max_length=255, help_text='Client public key for encryption')
    auth = models.CharField(max_length=255, help_text='Authentication secret')
    user_agent = models.CharField(max_length=255, blank=True, help_text='Browser / OS metadata')
    category_filter = models.CharField(
        max_length=30,
        default='all',
        help_text='Subscribed category filter (e.g. all, placement, circular)'
    )
    is_active = models.BooleanField(default=True, help_text='Whether this subscription is active')
    created_at = models.DateTimeField(auto_now_add=True)
    last_notified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Push Subscription'
        verbose_name_plural = 'Push Subscriptions'

    def __str__(self):
        return f"Subscription ({self.created_at.strftime('%Y-%m-%d')} - {self.category_filter})"

