import pytest
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from apps.accounts.models import AdminUser
from .models import Blog,Category
@pytest.mark.django_db
def test_editor_can_create_blog(client):
    user=AdminUser.objects.create_user(email='editor@example.com',password='safe-password',role='editor')
    client.force_login(user);category=Category.objects.create(name='AI')
    image=BytesIO();Image.new('RGB',(1,1),'white').save(image,format='PNG');image.seek(0)
    response=client.post(reverse('blog:add'),{'title':'Test post','slug':'test-post','author':user.pk,'category':category.pk,'content':'<p>Content</p>','tags':'ai','status':'draft','featured_image':SimpleUploadedFile('image.png',image.read(),content_type='image/png')})
    assert response.status_code==302
    assert Blog.objects.filter(slug='test-post').exists()
