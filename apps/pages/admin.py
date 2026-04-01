from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display  = ('first_name', 'last_name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('first_name', 'last_name', 'role')
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'greeting', 'avatar'),
        }),
        ('Kasbiy', {
            'fields': ('role', 'bio'),
        }),
        ('Havolalar', {
            'fields': ('cta_label', 'cta_link', 'telegram', 'instagram', 'github', 'linkedin'),
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_active'),
        }),
    )
