from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Bookshelf

@admin.register(Bookshelf)
class BookshelfAdmin(ModelAdmin):
    list_display = ('user', 'book', 'status', 'pages_read', 'added_at')
    list_filter = ('status', 'added_at')
    search_fields = ('user__username', 'book__title')
