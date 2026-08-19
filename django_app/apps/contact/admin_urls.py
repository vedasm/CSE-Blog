from django.urls import path
from .views import MessagesView
app_name='contact_admin'
urlpatterns=[path('messages/',MessagesView.as_view(),name='messages')]
