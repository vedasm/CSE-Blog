from django.urls import path
from .views import DeleteImageView,EditImageView,ManageGalleryView,UploadImageView
app_name='gallery'
urlpatterns=[path('gallery/',ManageGalleryView.as_view(),name='manage'),path('gallery/upload/',UploadImageView.as_view(),name='upload'),path('gallery/<int:pk>/edit/',EditImageView.as_view(),name='edit'),path('gallery/<int:pk>/delete/',DeleteImageView.as_view(),name='delete')]
