from django.urls import path
from .views import TeamMemberListView, MissionListView

urlpatterns = [
    path('team/', TeamMemberListView.as_view(), name='team-list'),
    path('mission/', MissionListView.as_view(), name='mission-list'),
]
