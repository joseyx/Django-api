from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import CustomUser as User
from .serializers import UserSerializer, ProfileSerializer, UserUpdateSerializer,  ProfileUpdateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, details=True)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, details=True)

        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user, details=True)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,
                'is_admin': user_serializer.data.get('profile', {}).get('is_admin', False)
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully."
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_serializer = UserSerializer(request.user)
        profile_serializer = ProfileSerializer(request.user.profile)
        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='token')
    def token(self, request):
        return TokenObtainPairView.as_view()(request._request)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='token/refresh')
    def token_refresh(self, request):
        return TokenRefreshView.as_view()(request._request)

    @action(detail=True, methods=['put'], permission_classes=[AllowAny], url_path='update-profile')
    def update_profile(self, request, pk=None):
        user = self.get_object()

        # Actualizar datos del usuario
        user_data = request.data.get('user', {})
        user_serializer = UserUpdateSerializer(instance=user, data=user_data, partial=True)

        # Actualizar datos del perfil
        profile_data = request.data.get('profile', {})
        profile_serializer = ProfileUpdateSerializer(instance=user.profile, data=profile_data, partial=True)

        user_valid = user_serializer.is_valid()
        profile_valid = profile_serializer.is_valid()

        if user_valid and profile_valid:
            user_serializer.save()
            profile_serializer.save()
            return Response({
                'user': user_serializer.data,
                'profile': profile_serializer.data
            }, status=status.HTTP_200_OK)

        errors = {}
        if not user_valid:
            errors.update(user_serializer.errors)
        if not profile_valid:
            errors.update(profile_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# Vista de prueba para verificar la autenticación
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Authenticated'}, status=status.HTTP_200_OK)