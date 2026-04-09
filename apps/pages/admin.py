from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import TeamMember, MissionSection, SubscriptionPlan


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
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelAdmin):
    list_display = ('name_uz', 'price_uzs', 'price_usd', 'order', 'is_active', 'is_free', 'is_most_popular')
    list_editable = ('order', 'is_active', 'is_most_popular', 'is_free')
    list_filter = ('is_active', 'is_free', 'is_most_popular')
    search_fields = ('name_uz', 'name_ru', 'name_en')

    fieldsets = (
        ('Uzbek (UZ)', {
            'fields': ('name_uz', 'description_uz', 'period_uz', 'features_uz', 'badge_text_uz', 'button_text_uz'),
        }),
        ('Russian (RU)', {
            'fields': ('name_ru', 'description_ru', 'period_ru', 'features_ru', 'badge_text_ru', 'button_text_ru'),
        }),
        ('English (EN)', {
            'fields': ('name_en', 'description_en', 'period_en', 'features_en', 'badge_text_en', 'button_text_en'),
        }),
        ('Pricing', {
            'fields': ('price_uzs', 'price_usd', 'is_free'),
        }),
        ('Settings', {
            'fields': ('is_most_popular', 'is_recommended', 'order', 'is_active'),
        }),
    )
