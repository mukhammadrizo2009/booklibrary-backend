from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import TeamMember, MissionSection
from .serializers import TeamMemberSerializer, MissionSerializer


class TeamMemberListView(ListAPIView):
    """Public endpoint — returns active team members sorted by order."""
    permission_classes = [AllowAny]
    serializer_class   = TeamMemberSerializer
    queryset           = TeamMember.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MissionListView(ListAPIView):
    """Public endpoint — returns the active mission section."""
    permission_classes = [AllowAny]
    serializer_class   = MissionSerializer
    queryset           = MissionSection.objects.filter(is_active=True).order_by('-id')[:1]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
