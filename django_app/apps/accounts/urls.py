from django.urls import path
from .views import AdminLoginView, AdminLogoutView
app_name = 'accounts'
urlpatterns = [path('login/', AdminLoginView.as_view(), name='login'), path('logout/', AdminLogoutView.as_view(), name='logout')]
