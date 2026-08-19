import io
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
class GalleryImage(models.Model):
    title=models.CharField(max_length=200); image=models.ImageField(upload_to='gallery/%Y/%m/')
    thumbnail=models.ImageField(upload_to='gallery/thumbs/', blank=True); category=models.CharField(max_length=100)
    uploaded_at=models.DateTimeField(auto_now_add=True); uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    class Meta: ordering=['-uploaded_at']
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and not self.thumbnail:
            image = Image.open(self.image.path).convert('RGB'); image.thumbnail((200,200), Image.Resampling.LANCZOS)
            data=io.BytesIO(); image.save(data, format='JPEG', quality=85)
            self.thumbnail.save(f'thumb_{self.pk}.jpg', ContentFile(data.getvalue()), save=False)
            super().save(update_fields=['thumbnail'])
    def __str__(self): return self.title
