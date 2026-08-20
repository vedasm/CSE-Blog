from django.urls import path
from .views import (
    NewsDetailView,
    NewsJsonFeedView,
    NewsListView,
    PushSubscribeView,
    PushUnsubscribeView,
    VapidPublicKeyView,
)

app_name = 'public_news'

urlpatterns = [
    path('', NewsListView.as_view(), name='list'),
    path('api/feed/', NewsJsonFeedView.as_view(), name='feed'),
    path('api/push/vapid-key/', VapidPublicKeyView.as_view(), name='vapid_key'),
    path('api/push/subscribe/', PushSubscribeView.as_view(), name='push_subscribe'),
    path('api/push/unsubscribe/', PushUnsubscribeView.as_view(), name='push_unsubscribe'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='detail'),
]
