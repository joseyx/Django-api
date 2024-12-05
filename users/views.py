import os

from PIL import Image
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


def resize_image(image_path):
    sizes = {
        'big': (1920, 1080),
        'medium': (1280, 720),
        'mini': (640, 360)
    }
    image = Image.open(image_path)
    resized_paths = {}
    base_dir = os.path.dirname(image_path)

    for size_name, size in sizes.items():
        resized_image = image.resize(size)
        resized_filename = f"{os.path.basename(image_path).rsplit('.', 1)[0]}_{size_name}.{image_path.rsplit('.', 1)[1]}"
        resized_path = os.path.join(base_dir, resized_filename)
        resized_image.save(resized_path)
        resized_paths[size_name] = os.path.relpath(resized_path, base_dir)
    return resized_paths


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

        # Normalizar los datos del usuario
        user_data = {
            key.replace('user[', '').replace(']', ''): value[0] if value else ''
            for key, value in request.data.lists()
            if key.startswith('user[')
        }
        profile_data = {
            key.replace('profile[', '').replace(']', ''): value[0] if value and value[0] else None
            for key, value in request.data.lists()
            if key.startswith('profile[')
        }

        # Eliminar claves con valores `None`
        profile_data = {k: v for k, v in profile_data.items() if v is not None}

        # Serializadores
        user_serializer = UserUpdateSerializer(instance=user, data=user_data, partial=True)
        profile_serializer = ProfileUpdateSerializer(instance=user.profile, data=profile_data, partial=True)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()

            # Revisamos si `imagen_perfil` es un archivo o una URL
            imagen_perfil_url = profile_data.get('imagen_perfil')
            imagen_perfil = request.FILES.get('profile[imagen_perfil]')

            if imagen_perfil_url:
                # Si la URL comienza con 'http', ignoramos cualquier operación de imagen
                if isinstance(imagen_perfil_url, str) and imagen_perfil_url.startswith('http'):
                    return Response({
                        'user': user_serializer.data,
                        'profile': profile_serializer.data
                    }, status=status.HTTP_200_OK)

            if imagen_perfil:
                # se guarda la imagen en el perfil
                user.profile.imagen_perfil = imagen_perfil
                user.profile.save()

                imagen_perfil = user.profile.imagen_perfil

                resized_paths = resize_image(imagen_perfil.path)
                user.profile.imagen_perfil_big = "profile_images/" + resized_paths['big']
                user.profile.imagen_perfil_medium = "profile_images/" + resized_paths['medium']
                user.profile.imagen_perfil_mini = "profile_images/" + resized_paths['mini']
                user.profile.save()

            return Response({
                'user': user_serializer.data,
                'profile': profile_serializer.data
            }, status=status.HTTP_200_OK)

        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not profile_serializer.is_valid():
            errors.update(profile_serializer.errors)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# Vista de prueba para verificar la autenticación
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Authenticated'}, status=status.HTTP_200_OK)