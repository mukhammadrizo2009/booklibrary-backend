from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView, RegisterView

router = DefaultRouter()
router.register(r'leaderboard', UserViewSet, basename='leaderboard')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
