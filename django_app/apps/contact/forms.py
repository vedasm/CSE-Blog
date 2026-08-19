from django.forms import ModelForm
from .models import ContactMessage
class ContactForm(ModelForm):
    class Meta: model=ContactMessage;fields=['name','email','message']
