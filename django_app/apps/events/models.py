from django.db import models


class Event(models.Model):
    class Category(models.TextChoices):
        WORKSHOP = 'workshop', 'Workshop'
        HACKATHON = 'hackathon', 'Hackathon'
        SEMINAR = 'seminar', 'Seminar'
        GUEST_LECTURE = 'guest_lecture', 'Guest Lecture'
        SYMPOSIUM = 'symposium', 'Symposium'
        CONFERENCE = 'conference', 'Conference'

    class Status(models.TextChoices):
        UPCOMING = 'upcoming', 'Upcoming'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'

    title = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=Category.choices)
    event_date = models.DateField()
    event_time = models.TimeField()
    venue = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/%Y/%m/', blank=True, null=True)
    description = models.TextField()
    registration_link = models.URLField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UPCOMING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date', 'event_time']

    def __str__(self):
        return self.title


class ScheduleItem(models.Model):
    class Category(models.TextChoices):
        EXAM = 'exam', 'Exam / Assessment'
        HACKATHON = 'hackathon', 'Hackathon / Contest'
        WORKSHOP = 'workshop', 'Workshop / Event'
        PLACEMENT = 'placement', 'Placement Drive'
        ACADEMIC = 'academic', 'Academic Milestone'
        HOLIDAY = 'holiday', 'Holiday / Vacation'
        DEADLINE = 'deadline', 'Submission Deadline'
        GENERAL = 'general', 'General Schedule'

    title = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.ACADEMIC)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Optional for multi-day schedules")
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    registration_link = models.URLField(blank=True)
    attachment = models.FileField(upload_to='schedules/%Y/%m/', blank=True, null=True)
    is_academic_calendar = models.BooleanField(default=False, help_text="Set to true for official academic calendar items")
    is_published = models.BooleanField(default=True)

    # Synchronization link to Event (ensures zero duplicates)
    source_event = models.OneToOneField(
        Event,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='schedule_item'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'start_time', 'title']
        verbose_name = 'Schedule Item'
        verbose_name_plural = 'Schedule Items'

    def __str__(self):
        return f"{self.title} ({self.start_date})"

    @property
    def is_multi_day(self):
        return bool(self.end_date and self.end_date != self.start_date)

    @property
    def category_color(self):
        color_map = {
            'exam': '#EF4444',      # Red
            'hackathon': '#8B5CF6', # Purple
            'workshop': '#365ACA',  # Blue
            'placement': '#10B981', # Green
            'academic': '#F59E0B',  # Amber
            'holiday': '#EC4899',   # Pink
            'deadline': '#F97316',  # Orange
            'general': '#64748B',   # Slate
        }
        return color_map.get(self.category, '#365ACA')
