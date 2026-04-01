from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import TeamMember, MissionSection


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('first_name_uz', 'role_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('first_name_uz', 'last_name_uz', 'role_uz')
    
    fieldsets = (
        ('Uzbek (UZ)', {
            'fields': ('greeting_uz', 'first_name_uz', 'last_name_uz', 'role_uz', 'bio_uz', 'cta_label_uz'),
        }),
        ('Russian (RU)', {
            'fields': ('greeting_ru', 'first_name_ru', 'last_name_ru', 'role_ru', 'bio_ru', 'cta_label_ru'),
        }),
        ('English (EN)', {
            'fields': ('greeting_en', 'first_name_en', 'last_name_en', 'role_en', 'bio_en', 'cta_label_en'),
        }),
        ('Media & Social', {
            'fields': ('avatar', 'cta_link', 'telegram', 'instagram', 'github', 'linkedin'),
        }),
        ('Settings', {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(MissionSection)
class MissionSectionAdmin(ModelAdmin):
    list_display = ('id', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('General', {
            'fields': ('logo', 'is_active'),
        }),
        ('Translations', {
            'fields': ('description_uz', 'description_ru', 'description_en'),
        }),
    )
