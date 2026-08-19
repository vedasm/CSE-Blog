from django.db import models
class ContactMessage(models.Model):
    name=models.CharField(max_length=100); email=models.EmailField(); message=models.TextField(); is_read=models.BooleanField(default=False)
    replied_at=models.DateTimeField(null=True, blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.name}: {self.email}'
