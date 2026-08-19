from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email: raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password); user.save(using=self._db); return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False); extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.update(is_staff=True, is_superuser=True, role='superadmin')
        return self._create_user(email, password, **extra_fields)

class AdminUser(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Super Admin'
        EDITOR = 'editor', 'Editor'
        VIEWER = 'viewer', 'Viewer'
        STUDENT = 'student', 'Student'
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.EDITOR)
    profile_picture = models.ImageField(upload_to='admins/', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = AdminUserManager()
    def __str__(self): return self.email

class LoginAttempt(models.Model):
    email = models.EmailField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
