from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import TeamMember
from .serializers import TeamMemberSerializer


class TeamMemberListView(ListAPIView):
    """Public endpoint — returns active team members sorted by order."""
    permission_classes = [AllowAny]
    serializer_class   = TeamMemberSerializer
    queryset           = TeamMember.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
