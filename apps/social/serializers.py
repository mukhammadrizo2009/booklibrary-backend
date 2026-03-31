from rest_framework import serializers
from .models import Follow, Activity, Message, MessageReaction, Post, PostLike, PostComment, AdBanner

class FollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.CharField(source='follower.username', read_only=True)
    following_name = serializers.CharField(source='following.username', read_only=True)
    
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['follower']

class ActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'


class MessageReactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MessageReaction
        fields = ['id', 'username', 'emoji']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_picture = serializers.SerializerMethodField()
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    # Reply preview fields
    reply_to_id = serializers.PrimaryKeyRelatedField(
        source='reply_to',
        queryset=Message.objects.all(),
        allow_null=True,
        required=False,
    )
    reply_preview = serializers.SerializerMethodField()
    reactions = MessageReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_username', 'sender_picture',
            'recipient', 'recipient_username', 'content',
            'reply_to_id', 'reply_preview', 'reactions',
            'is_read', 'is_edited', 'created_at', 'updated_at',
        ]
        read_only_fields = ['sender', 'is_read', 'is_edited', 'created_at', 'updated_at', 'reply_preview', 'reactions']

    def get_sender_picture(self, obj):
        request = self.context.get('request')
        if obj.sender.profile_picture and hasattr(obj.sender.profile_picture, 'url'):
            url = obj.sender.profile_picture.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_reply_preview(self, obj):
        if obj.reply_to:
            return {
                'id': obj.reply_to.id,
                'content': obj.reply_to.content[:120],
                'sender_username': obj.reply_to.sender.username,
            }
        return None

class PostCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id', 'user', 'username', 'profile_picture', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.user.profile_picture and hasattr(obj.user.profile_picture, 'url'):
            url = obj.user.profile_picture.url
            return request.build_absolute_uri(url) if request else url
        return None

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_picture = serializers.SerializerMethodField()
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_cover = serializers.SerializerMethodField()
    book_slug = serializers.CharField(source='book.slug', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    recent_comments = PostCommentSerializer(source='comments', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'username', 'profile_picture', 'post_type', 'content',
            'book', 'book_title', 'book_cover', 'book_slug', 'ad_link', 'created_at',
            'likes_count', 'comments_count', 'is_liked', 'recent_comments'
        ]
        read_only_fields = ['user', 'created_at']

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.user.profile_picture and hasattr(obj.user.profile_picture, 'url'):
            url = obj.user.profile_picture.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_book_cover(self, obj):
        request = self.context.get('request')
        if obj.book and obj.book.cover_image and hasattr(obj.book.cover_image, 'url'):
            url = obj.book.cover_image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class AdBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdBanner
        fields = '__all__'
