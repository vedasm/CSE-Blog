from django.urls import path
from .views import FacultyListView
app_name='public_faculty'
urlpatterns=[path('',FacultyListView.as_view(),name='list')]
