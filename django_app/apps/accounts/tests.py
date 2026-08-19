import pytest
from django.urls import reverse
from .models import AdminUser
@pytest.mark.django_db
def test_admin_login_success(client):
    AdminUser.objects.create_user(email='admin@example.com',password='safe-password',role='superadmin')
    response=client.post(reverse('accounts:login'),{'email':'admin@example.com','password':'safe-password'})
    assert response.status_code==302
    assert response.url==reverse('core:dashboard')
@pytest.mark.django_db
def test_admin_login_rejects_bad_credentials(client):
    response=client.post(reverse('accounts:login'),{'email':'nobody@example.com','password':'wrong'})
    assert response.status_code==200
    assert b'Invalid credentials' in response.content
