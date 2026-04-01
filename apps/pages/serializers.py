from rest_framework import serializers
from .models import TeamMember, MissionSection


class MissionSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = MissionSection
        fields = ['id', 'logo', 'logo_url', 'description_uz', 'description_ru', 'description_en', 'is_active']

    def get_logo_url(self, obj):
        if not obj.logo:
            return ''
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.logo.url)
        return obj.logo.url


class TeamMemberSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            'id', 'greeting', 'first_name', 'last_name',
            'role', 'bio', 'avatar_url',
            'cta_label', 'cta_link',
            'telegram', 'instagram', 'github', 'linkedin',
            'order',
        ]

    def get_avatar_url(self, obj):
        if not obj.avatar:
            return ''
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.avatar.url)
        return obj.avatar.url
