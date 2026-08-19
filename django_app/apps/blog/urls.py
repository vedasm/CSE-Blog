from django.urls import path
from .views import (
    BlogDetailView,
    BlogListView,
    StudentBlogListView,
    StudentBlogCreateView,
    StudentBlogUpdateView,
    StudentBlogSubmitView,
    StudentBlogDetailView,
)
app_name='public_blog'
urlpatterns=[
    path('',BlogListView.as_view(),name='list'),
    path('my/', StudentBlogListView.as_view(), name='my_blogs'),
    path('create/', StudentBlogCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', StudentBlogUpdateView.as_view(), name='edit'),
    path('<int:pk>/submit/', StudentBlogSubmitView.as_view(), name='submit'),
    path('<int:pk>/', StudentBlogDetailView.as_view(), name='student_detail'),
    path('<slug:slug>/',BlogDetailView.as_view(),name='detail'),
]
