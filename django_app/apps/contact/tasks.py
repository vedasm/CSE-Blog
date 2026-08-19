from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import ContactMessage
@shared_task
def send_contact_notification(message_id):
    msg=ContactMessage.objects.get(pk=message_id)
    send_mail(f'New Contact Message from {msg.name}',msg.message,settings.DEFAULT_FROM_EMAIL,[settings.CONTACT_NOTIFY_EMAIL])
