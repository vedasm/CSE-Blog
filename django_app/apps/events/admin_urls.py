from django.urls import path
from .views import (
    AddEventView,
    DeleteEventView,
    EditEventView,
    ManageEventsView,
    AddScheduleView,
    DeleteScheduleView,
    EditScheduleView,
    ManageSchedulesView,
)

app_name = 'events'

urlpatterns = [
    # Event Management
    path('events/', ManageEventsView.as_view(), name='manage'),
    path('events/add/', AddEventView.as_view(), name='add'),
    path('events/<int:pk>/edit/', EditEventView.as_view(), name='edit'),
    path('events/<int:pk>/delete/', DeleteEventView.as_view(), name='delete'),

    # Academic Calendar & Schedules Management
    path('calendar/', ManageSchedulesView.as_view(), name='admin_schedules'),
    path('calendar/add/', AddScheduleView.as_view(), name='add_schedule'),
    path('calendar/<int:pk>/edit/', EditScheduleView.as_view(), name='edit_schedule'),
    path('calendar/<int:pk>/delete/', DeleteScheduleView.as_view(), name='delete_schedule'),
]
