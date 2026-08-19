from django.urls import path
from .views import NewsDetailView, NewsJsonFeedView, NewsListView

app_name = 'public_news'

urlpatterns = [
    path('', NewsListView.as_view(), name='list'),
    path('api/feed/', NewsJsonFeedView.as_view(), name='feed'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='detail'),
]
