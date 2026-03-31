from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookshelfViewSet, BookCollectionViewSet

router = DefaultRouter()
router.register(r'bookshelves', BookshelfViewSet, basename='bookshelf')
router.register(r'collections', BookCollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
]
