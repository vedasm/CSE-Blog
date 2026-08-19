import pytest
from unittest.mock import patch
from django.urls import reverse
from .models import ContactMessage
@pytest.mark.django_db
@patch('apps.contact.views.send_contact_notification.delay')
def test_contact_form_saves_message(send_task,client):
    response=client.post(reverse('contact:contact'),{'name':'Student','email':'student@example.com','message':'Please share more event information.'})
    assert response.status_code==302
    assert ContactMessage.objects.filter(email='student@example.com').exists()
    send_task.assert_called_once()
