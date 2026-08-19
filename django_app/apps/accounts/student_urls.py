from django.urls import path
from .views import StudentRegisterView, StudentLoginView, StudentLogoutView

app_name = 'student_accounts'

urlpatterns = [
    path('register/', StudentRegisterView.as_view(), name='register'),
    path('login/', StudentLoginView.as_view(), name='login'),
    path('logout/', StudentLogoutView.as_view(), name='logout'),
]
