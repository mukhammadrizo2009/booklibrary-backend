from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FollowViewSet, ActivityViewSet, MessageViewSet, PostViewSet, AdBannerViewSet

router = DefaultRouter()
router.register(r'follows', FollowViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'ads', AdBannerViewSet, basename='ads')

urlpatterns = [
    path('', include(router.urls)),
]
