from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'points', 'is_pro', 'is_staff')
    list_editable = ('is_pro',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Library Profile', {'fields': ('bio', 'profile_picture', 'points', 'total_pages_read', 'is_pro')}),
    )

