from django.urls import path
from .views import (
    HomeView,
    PlacementsView,
    ResearchView,
    AchievementsView,
    InfrastructureView,
    AlumniView,
    DashboardView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('placements/', PlacementsView.as_view(), name='placements'),
    path('research/', ResearchView.as_view(), name='research'),
    path('achievements/', AchievementsView.as_view(), name='achievements'),
    path('infrastructure/', InfrastructureView.as_view(), name='infrastructure'),
    path('alumni/', AlumniView.as_view(), name='alumni'),
    path('admin/dashboard/', DashboardView.as_view(), name='dashboard'),
]
