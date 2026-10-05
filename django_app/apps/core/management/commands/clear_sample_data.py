from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.accounts.models import LoginAttempt
from apps.blog.models import Blog, Category
from apps.contact.models import ContactMessage
from apps.core.models import (
    DepartmentDocument,
    DepartmentLab,
    DepartmentMilestone,
    PlacementStat,
    SiteSettings,
)
from apps.events.models import Event, ScheduleItem
from apps.faculty.models import Faculty
from apps.gallery.models import GalleryImage
from apps.news.models import NewsItem, PushSubscription


CONTENT_MODELS = (
    LoginAttempt,
    ContactMessage,
    PushSubscription,
    Blog,
    Category,
    NewsItem,
    Event,
    ScheduleItem,
    Faculty,
    GalleryImage,
    DepartmentDocument,
    PlacementStat,
    DepartmentLab,
    DepartmentMilestone,
    SiteSettings,
)


class Command(BaseCommand):
    help = 'Delete application content while preserving all admin and student accounts.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Required confirmation for this destructive operation.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not options['confirm']:
            raise CommandError(
                'This deletes application content. Re-run with --confirm to continue.'
            )

        deleted = {}
        for model in CONTENT_MODELS:
            count, _ = model.objects.all().delete()
            deleted[model._meta.label] = count

        total = sum(deleted.values())
        self.stdout.write(self.style.SUCCESS(
            f'Deleted {total} application records; user accounts were preserved.'
        ))
        for label, count in deleted.items():
            if count:
                self.stdout.write(f'  {label}: {count}')
