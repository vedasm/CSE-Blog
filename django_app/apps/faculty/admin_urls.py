from django.urls import path
from .views import AddFacultyView,DeleteFacultyView,EditFacultyView,ManageFacultyView
app_name='faculty'
urlpatterns=[path('faculty/',ManageFacultyView.as_view(),name='manage'),path('faculty/add/',AddFacultyView.as_view(),name='add'),path('faculty/<int:pk>/edit/',EditFacultyView.as_view(),name='edit'),path('faculty/<int:pk>/delete/',DeleteFacultyView.as_view(),name='delete')]
