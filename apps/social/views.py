from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.users.permissions import IsProUser

from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Follow, Activity, Message, MessageReaction, Post, PostLike, PostComment, AdBanner
from .serializers import FollowSerializer, ActivitySerializer, MessageSerializer, MessageReactionSerializer, PostSerializer, PostCommentSerializer, AdBannerSerializer

User = get_user_model()

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all().order_by('-created_at')
    serializer_class = ActivitySerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsProUser]


    def get_queryset(self):
        user = self.request.user
        other_username = self.request.query_params.get('with')
        if other_username:
            try:
                other = User.objects.get(username=other_username)
                return Message.objects.filter(
                    Q(sender=user, recipient=other) | Q(sender=other, recipient=user)
                )
            except User.DoesNotExist:
                return Message.objects.none()
        return Message.objects.filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    # ── Edit a message (only sender can edit) ─────────────────────────────────
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sender != request.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        new_content = request.data.get('content', '').strip()
        if not new_content:
            return Response({'error': 'Content cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.content = new_content
        instance.is_edited = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # ── Delete a message (only sender can delete) ─────────────────────────────
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sender != request.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ── React to a message ────────────────────────────────────────────────────
    @action(detail=True, methods=['post'])
    def react(self, request, pk=None):
        msg = self.get_object()
        emoji = request.data.get('emoji')
        if not emoji:
            return Response({'error': 'emoji is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        reaction = MessageReaction.objects.filter(message=msg, user=request.user).first()
        if reaction:
            if reaction.emoji == emoji:
                reaction.delete()
            else:
                reaction.emoji = emoji
                reaction.save()
        else:
            MessageReaction.objects.create(message=msg, user=request.user, emoji=emoji)
        
        # Return updated message
        return Response(self.get_serializer(msg).data)

    # ── Conversations list ────────────────────────────────────────────────────
    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """Returns unique conversation partners with last message."""
        user = request.user
        messages = Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-created_at')
        seen = set()
        result = []
        for msg in messages:
            other = msg.recipient if msg.sender == user else msg.sender
            if other.id not in seen:
                seen.add(other.id)
                unread = Message.objects.filter(sender=other, recipient=user, is_read=False).count()
                result.append({
                    'user_id': other.id,
                    'username': other.username,
                    'first_name': other.first_name,
                    'last_name': other.last_name,
                    'profile_picture': request.build_absolute_uri(other.profile_picture.url) if other.profile_picture else None,
                    'last_message': msg.content,
                    'last_message_time': msg.created_at,
                    'unread_count': unread,
                    'is_mine': msg.sender == user,
                })
        return Response(result)

    # ── Mark messages as read ─────────────────────────────────────────────────
    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        """Mark all messages from a user as read."""
        sender_username = request.data.get('username')
        if not sender_username:
            return Response({'error': 'username required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sender = User.objects.get(username=sender_username)
            Message.objects.filter(sender=sender, recipient=request.user, is_read=False).update(is_read=True)
            return Response({'ok': True})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # ── Clear entire chat with a user ─────────────────────────────────────────
    @action(detail=False, methods=['delete'])
    def clear_chat(self, request):
        """Delete ALL messages between current user and given username."""
        other_username = request.query_params.get('with')
        if not other_username:
            return Response({'error': 'with param required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            other = User.objects.get(username=other_username)
            Message.objects.filter(
                Q(sender=request.user, recipient=other) | Q(sender=other, recipient=request.user)
            ).delete()
            return Response({'ok': True})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like = PostLike.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
        else:
            PostLike.objects.create(post=post, user=request.user)
        return Response(self.get_serializer(post).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()
        content = request.data.get('content')
        if not content:
            return Response({'error': 'content is required'}, status=status.HTTP_400_BAD_REQUEST)
        PostComment.objects.create(post=post, user=request.user, content=content)
        return Response(self.get_serializer(post).data)

class AdBannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdBanner.objects.filter(is_active=True).order_by('?')
    serializer_class = AdBannerSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def active(self, request):
        banners = self.get_queryset()
        return Response(self.get_serializer(banners, many=True).data)

