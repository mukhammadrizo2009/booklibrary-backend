from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from .models import Category, Book, Review
from .serializers import CategorySerializer, BookSerializer, ReviewSerializer
from apps.library.models import Bookshelf

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Allow lookup by slug OR by pk (numeric id)
    lookup_field = 'pk'

    def get_object(self):
        """If pk looks like a slug (non-numeric), lookup by slug."""
        pk = self.kwargs.get('pk', '')
        if not str(pk).isdigit():
            from rest_framework.generics import get_object_or_404
            obj = get_object_or_404(Book, slug=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()

    @action(detail=False, methods=['get'])
    def trending(self, request):
        one_week_ago = timezone.now() - timedelta(days=7)
        trending_books = Book.objects.annotate(
            recent_reviews=Count('reviews', filter=models.Q(reviews__created_at__gte=one_week_ago))
        ).filter(recent_reviews__gt=0).order_by('-recent_reviews')[:3]
        
        if not trending_books.exists():
            trending_books = Book.objects.annotate(
                rev_count=Count('reviews')
            ).order_by('-rev_count', '-id')[:3]
            
        serializer = self.get_serializer(trending_books, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # For direct detail view, allow fetching any book
        if self.action == 'retrieve':
            queryset = Book.objects.all()
        else:
            added_by = self.request.query_params.get('added_by')
            
            # If we are looking for a specific user's books (Profile)
            if added_by:
                queryset = Book.objects.filter(added_by_id=added_by)
                # If viewing someone else's books, only show those that are Public on their shelf
                if self.request.user.is_anonymous or str(added_by) != str(self.request.user.id):
                    queryset = queryset.filter(shelved_by__user_id=added_by, shelved_by__is_public=True)
                return queryset.distinct().annotate(
                    avg_rating=Coalesce(Avg('reviews__rating'), 0, output_field=models.FloatField()),
                    rev_count=Count('reviews')
                )
                
            # Global Explore: Official or Applied
            queryset = Book.objects.filter(
                models.Q(added_by__isnull=True) | 
                models.Q(shelved_by__is_applied_to_explore=True)
            ).distinct()
        
        # Filtering (only for list view usually, but retrieve will skip these if no params)
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        category = self.request.query_params.get('category')
        added_by = self.request.query_params.get('added_by')
        search = self.request.query_params.get('search')
        following = self.request.query_params.get('following')

        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(author__icontains=search)
            )
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if added_by:
            if added_by.isdigit():
                queryset = queryset.filter(added_by_id=added_by)
            else:
                queryset = queryset.filter(
                    models.Q(added_by__username__icontains=added_by) |
                    models.Q(added_by__first_name__icontains=added_by) |
                    models.Q(added_by__last_name__icontains=added_by)
                )
        
        if following == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(added_by__follower_users=self.request.user)
        
        # Annotate with average rating and count for sorting
        queryset = queryset.annotate(
            avg_rating=Coalesce(Avg('reviews__rating'), 0, output_field=models.FloatField()),
            rev_count=Count('reviews')
        ).order_by('-avg_rating', '-rev_count', '-id')

        return queryset.select_related('category', 'added_by')

    def perform_create(self, serializer):
        book = serializer.save(added_by=self.request.user)
        reading_status = self.request.data.get('reading_status')
        is_public = self.request.data.get('is_public', 'true') == 'true'
        is_applied = self.request.data.get('is_applied_to_explore', 'true') == 'true'
        
        if reading_status:
            Bookshelf.objects.update_or_create(
                user=self.request.user,
                book=book,
                defaults={
                    'status': reading_status,
                    'is_public': is_public,
                    'is_applied_to_explore': is_applied
                }
            )

    def perform_update(self, serializer):
        book = serializer.save()
        reading_status = self.request.data.get('reading_status')
        is_public = self.request.data.get('is_public', 'true') == 'true'
        is_applied = self.request.data.get('is_applied_to_explore', 'true') == 'true'
        
        if reading_status:
            Bookshelf.objects.update_or_create(
                user=self.request.user,
                book=book,
                defaults={
                    'status': reading_status,
                    'is_public': is_public,
                    'is_applied_to_explore': is_applied
                }
            )

    def destroy(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status
        instance = self.get_object()
        if instance.added_by != request.user and not request.user.is_staff:
            return Response({"detail": "Siz faqat o'zingiz qo'shgan kitoblarni o'chirishingiz mumkin."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status
        instance = self.get_object()
        if instance.added_by != request.user and not request.user.is_staff:
            return Response({"detail": "Siz faqat o'zingiz qo'shgan kitoblarni tahrirlashingiz mumkin."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        book_id = self.request.query_params.get('book')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        
        time_range = self.request.query_params.get('time_range')
        if time_range == 'week':
            one_week_ago = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(created_at__gte=one_week_ago)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
