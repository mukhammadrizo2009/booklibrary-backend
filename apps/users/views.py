from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
import requests
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            pic_url = request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
            return Response({
                'token': token.key, 
                'username': user.username, 
                'id': user.id,
                'profile_picture': pic_url,
                'is_pro': user.is_pro
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        login_id = request.data.get('username')
        password = request.data.get('password')
        
        # Try username login
        user = authenticate(username=login_id, password=password)
        
        # If failed, try email login
        if not user:
            try:
                user_obj = User.objects.get(email=login_id)
                user = authenticate(username=user_obj.username, password=password)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass
                
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            pic_url = request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
            return Response({
                'token': token.key, 
                'username': user.username, 
                'id': user.id,
                'profile_picture': pic_url,
                'is_pro': user.is_pro
            })

        return Response({'error': 'Invalid username/email or password'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class SupabaseGoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({"error": "No access_token provided."}, status=400)
            
        supabase_url = getattr(settings, 'SUPABASE_URL', '')
        supabase_anon_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'apikey': supabase_anon_key
        }
        res = requests.get(f"{supabase_url}/auth/v1/user", headers=headers)
        if res.status_code != 200:
            return Response({"error": "Invalid Supabase token"}, status=401)
            
        user_data = res.json()
        email = user_data.get('email')
        
        if not email:
            return Response({"error": "No email in token"}, status=400)
            
        # Get or create user safely
        full_name = user_data.get('user_metadata', {}).get('full_name', '')
        first_name = full_name.split(' ')[0] if full_name else email.split('@')[0]
        
        user = User.objects.filter(email=email).first()
        if not user:
            username_base = email.split('@')[0]
            username = username_base
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{username_base}{counter}"
                counter += 1
                
            user = User.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                is_active=True
            )
            user.set_unusable_password()
            user.save()
            
        token, _ = Token.objects.get_or_create(user=user)
        pic_url = request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
        return Response({
            'token': token.key, 
            'username': user.username, 
            'id': user.id,
            'profile_picture': pic_url,
            'is_pro': user.is_pro
        })

from django.utils import timezone
from datetime import timedelta

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if username and username != request.user.username:
            return Response({"detail": "You cannot edit another user's profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if username and username != request.user.username:
            return Response({"detail": "You cannot edit another user's profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = User.objects.all()
        timeframe = self.request.query_params.get('timeframe', 'all')
        
        # Currently, points are global. For real timeframes, we'd annotate sums of activities.
        # As a placeholder, we return all users sorted descending. 
        # In a full-blown system, you would JOIN on Activity logs.
        if timeframe == 'week':
            queryset = queryset.filter(date_joined__gte=timezone.now() - timedelta(days=7))
        elif timeframe == 'month':
            queryset = queryset.filter(date_joined__gte=timezone.now() - timedelta(days=30))
            
        # Social filtering
        followers_of = self.request.query_params.get('followers_of')
        if followers_of:
            queryset = queryset.filter(following_users__id=followers_of)
            
        followed_by = self.request.query_params.get('followed_by')
        if followed_by:
            queryset = queryset.filter(follower_users__id=followed_by)

        return queryset.order_by('-points')

    @action(detail=False, methods=['get'])
    def active_weekly(self, request):
        one_week_ago = timezone.now() - timedelta(days=7)
        from django.db.models import Count, Q
        
        active_users = User.objects.annotate(
            recent_posts=Count('posts', filter=Q(posts__created_at__gte=one_week_ago)),
            recent_activities=Count('activities', filter=Q(activities__created_at__gte=one_week_ago))
        ).order_by('-recent_posts', '-recent_activities', '-points')[:3]
        
        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, username=None):
        user_to_follow = self.get_object()
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        from apps.social.models import Follow
        follow_query = Follow.objects.filter(follower=request.user, following=user_to_follow)
        
        if follow_query.exists():
            follow_query.delete()
            is_following = False
        else:
            Follow.objects.create(follower=request.user, following=user_to_follow)
            is_following = True
            
        followers_count = Follow.objects.filter(following=user_to_follow).count()
        return Response({
            "is_following": is_following, 
            "followers_count": followers_count
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)