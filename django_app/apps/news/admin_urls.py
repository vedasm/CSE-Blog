from django.urls import path
from .views import AddNewsView, DeleteNewsView, EditNewsView, ManageNewsView, TogglePinNewsView

app_name = 'news'

urlpatterns = [
    path('news/', ManageNewsView.as_view(), name='manage'),
    path('news/add/', AddNewsView.as_view(), name='add'),
    path('news/<int:pk>/edit/', EditNewsView.as_view(), name='edit'),
    path('news/<int:pk>/delete/', DeleteNewsView.as_view(), name='delete'),
    path('news/<int:pk>/toggle-pin/', TogglePinNewsView.as_view(), name='toggle_pin'),
]
