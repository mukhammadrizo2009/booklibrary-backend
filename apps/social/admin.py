from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Follow, Activity, Message, MessageReaction, Post, PostLike, PostComment, AdBanner

@admin.register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')

@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ('user', 'activity_type', 'book', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'book__title')

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'recipient__username', 'content')

@admin.register(MessageReaction)
class MessageReactionAdmin(ModelAdmin):
    list_display = ('message', 'user', 'emoji')
    search_fields = ('user__username', 'emoji')

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('user', 'post_type', 'content', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('user__username', 'content')

@admin.register(PostLike)
class PostLikeAdmin(ModelAdmin):
    list_display = ('post', 'user', 'created_at')

@admin.register(PostComment)
class PostCommentAdmin(ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')

@admin.register(AdBanner)
class AdBannerAdmin(ModelAdmin):
    list_display = ('title', 'button_text', 'link', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
