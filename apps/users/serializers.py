import re
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='follower_users.count', read_only=True)
    following_count = serializers.IntegerField(source='following_users.count', read_only=True)
    books_read_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'bio', 'profile_picture', 'points', 'total_pages_read', 'followers_count', 'following_count', 'books_read_count', 'is_following', 'is_pro']
        read_only_fields = ['points', 'total_pages_read', 'is_pro']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None


    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.follower_users.filter(id=request.user.id).exists()
        return False

    def get_books_read_count(self, obj):
        return obj.shelves.filter(status='finished').count()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True, min_length=2, max_length=30)
    last_name = serializers.CharField(required=False, min_length=2, max_length=30, allow_blank=True)
    username = serializers.CharField(min_length=3, max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'date_of_birth']

    def validate_username(self, value):
        normalized_value = value.lower()
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9._]*$', normalized_value):
            raise serializers.ValidationError("Username must start with a letter and contain only letters, numbers, dots, or underscores.")
        if User.objects.filter(username__iexact=normalized_value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return normalized_value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_first_name(self, value):
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\'-]+$', value):
            raise serializers.ValidationError("First name should contain only letters.")
        return value

    def validate_last_name(self, value):
        if value and not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\'-]+$', value):
            raise serializers.ValidationError("Last name should contain only letters.")
        return value

    def validate_password(self, value):
        if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one letter and one number.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            date_of_birth=validated_data.get('date_of_birth')
        )
        return user
