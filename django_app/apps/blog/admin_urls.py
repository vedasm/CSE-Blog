from django.urls import path
from .views import (
    AddBlogView,
    DeleteBlogView,
    EditBlogView,
    ManageBlogsView,
    AdminBlogDetailView,
    AdminBlogApproveView,
    AdminBlogRejectView,
    AdminBlogPublishView,
    AdminBlogUnpublishView,
)
app_name='blog'
urlpatterns=[
    path('blogs/',ManageBlogsView.as_view(),name='manage'),
    path('blogs/add/',AddBlogView.as_view(),name='add'),
    path('blogs/<int:pk>/edit/',EditBlogView.as_view(),name='edit'),
    path('blogs/<int:pk>/delete/',DeleteBlogView.as_view(),name='delete'),
    path('blogs/<int:pk>/',AdminBlogDetailView.as_view(),name='detail'),
    path('blogs/<int:pk>/approve/',AdminBlogApproveView.as_view(),name='approve'),
    path('blogs/<int:pk>/reject/',AdminBlogRejectView.as_view(),name='reject'),
    path('blogs/<int:pk>/publish/',AdminBlogPublishView.as_view(),name='publish'),
    path('blogs/<int:pk>/unpublish/',AdminBlogUnpublishView.as_view(),name='unpublish'),
]
