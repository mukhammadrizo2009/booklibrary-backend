from rest_framework import serializers
from .models import Bookshelf
from apps.books.serializers import BookSerializer

class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['book'] = BookSerializer(instance.book, context=self.context).data
        return representation

from .models import BookCollection
from apps.books.models import Book

class BookCollectionSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    book_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Book.objects.all(), 
        source='books', 
        write_only=True,
        required=False
    )

    class Meta:
        model = BookCollection
        fields = ['id', 'user', 'name', 'description', 'books', 'book_ids', 'is_public', 'created_at']
        read_only_fields = ['user', 'created_at']
