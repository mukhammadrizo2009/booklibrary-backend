from rest_framework import viewsets, permissions
from .models import Bookshelf
from .serializers import BookshelfSerializer

class BookshelfViewSet(viewsets.ModelViewSet):
    serializer_class = BookshelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Bookshelf.objects.all().order_by('-added_at')
        user_id = self.request.query_params.get('user')
        status = self.request.query_params.get('status')
        book_id = self.request.query_params.get('book')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            # If viewing someone else's shelf, only show public items
            if self.request.user.is_anonymous or str(user_id) != str(self.request.user.id):
                queryset = queryset.filter(is_public=True)
        else:
            queryset = queryset.filter(user=self.request.user)
            
        if status:
            queryset = queryset.filter(status=status)
        if book_id:
            queryset = queryset.filter(book_id=book_id)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from .models import BookCollection
from .serializers import BookCollectionSerializer

class BookCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = BookCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = BookCollection.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            if self.request.user.is_anonymous or str(user_id) != str(self.request.user.id):
                queryset = queryset.filter(is_public=True)
        else:
            queryset = queryset.filter(user=self.request.user)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
