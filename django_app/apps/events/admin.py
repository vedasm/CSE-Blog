from django.contrib import admin
from .models import Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin): list_display=('title','category','event_date','status'); list_filter=('category','status'); search_fields=('title','venue')
