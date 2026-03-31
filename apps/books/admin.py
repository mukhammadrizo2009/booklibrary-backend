from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Book, Review

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'author', 'category', 'pages', 'published_date')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author', 'isbn')

@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username')
