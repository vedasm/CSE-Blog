from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, ScheduleItem


@receiver(post_save, sender=Event)
def sync_event_to_schedule(sender, instance, created, **kwargs):
    """
    Automatically syncs an Event to a ScheduleItem to guarantee no duplicates
    and ensure all events, hackathons, seminars, etc. appear on the calendar.
    """
    category_mapping = {
        Event.Category.HACKATHON: ScheduleItem.Category.HACKATHON,
        Event.Category.WORKSHOP: ScheduleItem.Category.WORKSHOP,
        Event.Category.SEMINAR: ScheduleItem.Category.WORKSHOP,
        Event.Category.GUEST_LECTURE: ScheduleItem.Category.WORKSHOP,
        Event.Category.SYMPOSIUM: ScheduleItem.Category.HACKATHON,
        Event.Category.CONFERENCE: ScheduleItem.Category.ACADEMIC,
    }
    target_category = category_mapping.get(instance.category, ScheduleItem.Category.WORKSHOP)

    ScheduleItem.objects.update_or_create(
        source_event=instance,
        defaults={
            'title': instance.title,
            'category': target_category,
            'start_date': instance.event_date,
            'start_time': instance.event_time,
            'venue': instance.venue or '',
            'description': instance.description or '',
            'registration_link': instance.registration_link or '',
            'is_published': True,
            'is_academic_calendar': False,
        }
    )
