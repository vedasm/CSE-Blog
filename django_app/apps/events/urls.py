from django.urls import path
from .views import EventListView, PublicCalendarView, ScheduleJsonFeedView

app_name = 'public_events'

urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('calendar/', PublicCalendarView.as_view(), name='calendar'),
    path('api/calendar/', ScheduleJsonFeedView.as_view(), name='calendar_feed'),
]
