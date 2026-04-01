from rest_framework import serializers
from .models import TeamMember


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
