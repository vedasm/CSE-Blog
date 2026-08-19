from django.db import models


class Faculty(models.Model):
    class Designation(models.TextChoices):
        PROFESSOR = 'professor', 'Professor'
        ASSOCIATE = 'associate_professor', 'Associate Professor'
        ASSISTANT = 'assistant_professor', 'Assistant Professor'

    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=24, choices=Designation.choices)
    specialization = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    scholar_link = models.URLField(blank=True)
    profile_link = models.URLField(
        max_length=500,
        blank=True,
        help_text='IRINS Profile URL (e.g. https://srmvalliammai.irins.org/profile/177877)'
    )
    photo = models.ImageField(upload_to='faculty/', blank=True, null=True)
    bio = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name
