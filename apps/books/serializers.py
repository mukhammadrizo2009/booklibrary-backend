from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Book, Review
from apps.library.models import Bookshelf

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)
    added_by_first_name = serializers.CharField(source='added_by.first_name', read_only=True)
    added_by_last_name = serializers.CharField(source='added_by.last_name', read_only=True)
    added_by_id = serializers.IntegerField(source='added_by.id', read_only=True)
    user_reading_status = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['added_by', 'slug']

    def get_cover_image(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def get_user_reading_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            shelf = Bookshelf.objects.filter(user=request.user, book=obj).first()
            return shelf.status if shelf else None
        return None

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_profile_picture = serializers.SerializerMethodField()
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_slug = serializers.CharField(source='book.slug', read_only=True)
    
    def get_user_profile_picture(self, obj):
        if obj.user.profile_picture:
            return obj.user.profile_picture.url
        return None
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']
