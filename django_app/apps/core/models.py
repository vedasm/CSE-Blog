from django.db import models


class SiteSettings(models.Model):
    internships = models.PositiveIntegerField(default=120)
    publications = models.PositiveIntegerField(default=65)
    hackathon_winners = models.PositiveIntegerField(default=40)
    placement_rate = models.PositiveIntegerField(default=98)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'site settings'

    @classmethod
    def current(cls):
        return cls.objects.get_or_create(pk=1)[0]


class DepartmentDocument(models.Model):
    class Category(models.TextChoices):
        PLACEMENT = 'placement', 'Placements'
        RESEARCH = 'research', 'Research & Journals'
        ACHIEVEMENT = 'achievement', 'Achievements'
        EVENT_ARCHIVE = 'event_archive', 'Events Archive'
        LABORATORY = 'laboratory', 'Laboratories & Facilities'
        LIBRARY = 'library', 'Library'
        ALUMNI = 'alumni', 'Alumni (SHIMMER)'
        GENERAL = 'general', 'General'

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.GENERAL)
    academic_year = models.CharField(max_length=50, blank=True, help_text='e.g. 2022-2023, 2021-2023, 2018-2020')
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='department_docs/', blank=True, null=True)
    external_url = models.URLField(blank=True, max_length=500, help_text='Direct PDF link from official server if file not uploaded locally')
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'display_order', '-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

    @property
    def download_url(self):
        if self.pdf_file:
            return self.pdf_file.url
        return self.external_url or '#'


class PlacementStat(models.Model):
    year = models.IntegerField(unique=True, help_text='e.g. 2023, 2022, 2021...')
    students_placed = models.PositiveIntegerField()
    total_offers = models.PositiveIntegerField(default=0, blank=True)
    highest_package = models.CharField(max_length=50, blank=True, default='')
    average_package = models.CharField(max_length=50, blank=True, default='')
    top_recruiters = models.TextField(blank=True, default='TCS, CTS, Wipro, Infosys, Zoho, Accenture, HCL, Cognizant')
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"Year {self.year}: {self.students_placed} Placed"


class DepartmentLab(models.Model):
    name = models.CharField(max_length=200)
    domain = models.CharField(max_length=255, blank=True)
    computers_count = models.PositiveIntegerField(default=35)
    printers_count = models.PositiveIntegerField(default=3)
    ups_info = models.CharField(max_length=100, default='10 KVA')
    software_installed = models.TextField(default='Oracle, Visual Basic, MS Office, Java')
    image_url = models.CharField(max_length=500, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class DepartmentMilestone(models.Model):
    title = models.CharField(max_length=100)
    metric_value = models.CharField(max_length=50, help_text='e.g. 25+, 149+, 8, 100+, 724+')
    icon = models.CharField(max_length=100, default='fa-solid fa-award')
    description = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return f"{self.title}: {self.metric_value}"
