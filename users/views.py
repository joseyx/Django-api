from django.http import Http404

from .models import CustomUser as User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework import status, generics

from users.serializers import UserSerializer, ProfileSerializer, UserUpdateSerializer, UserLoginSerializer, \
    ProfileUpdateSerializer


# Vista para el inicio de sesión
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserLoginSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,
                'is_admin': user.profile.is_admin
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Vista para el registro de usuarios
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully."
        }, status=status.HTTP_201_CREATED)

# Vista para obtener los datos del usuario autenticado
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        profile_serializer = ProfileSerializer(request.user.profile)
        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data
        })

# Vista para actualizar los datos de un usuario por su id
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404("User does not exist")

        user_data = request.data.get('user')
        profile_data = request.data.get('profile')

        if not profile_data:
            return Response({"profile": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserUpdateSerializer(user, data=user_data)
        profile_serializer = ProfileUpdateSerializer(user.profile, data=profile_data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response({
                'user': user_serializer.data,
                'profile': profile_serializer.data
            })

        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not profile_serializer.is_valid():
            errors.update(profile_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
# Vista para eliminar al usuario autenticado
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vista para obtener la lista de todos los usuarios con sus perfiles
class UserListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        user_data = []

        for user in users:
            user_serializer = UserSerializer(user)
            profile_serializer = ProfileSerializer(user.profile)
            user_data.append({
                'user': user_serializer.data,
                'profile': profile_serializer.data
            })

        return Response(user_data, status=status.HTTP_200_OK)

# Vista para obtener los datos de un usuario específico
class UserDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404("User does not exist")

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(user.profile)
        if profile_serializer.data['imagen_perfil'] == '':
            profile_serializer.data['imagen_perfil'] = user.profile.DEFAULT_IMAGE_PATH

        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data
        })
# Vista de prueba para verificar la autenticación
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Authenticated'}, status=status.HTTP_200_OK)