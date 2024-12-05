from .models import CustomUser as User
from rest_framework import serializers
from .models import Profile

# Serializer para la creación y serialización de usuarios

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Serializer para la actualización de usuarios
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

# Serializer para la serialización de perfiles
class ProfileSerializer(serializers.ModelSerializer):
    # Campos de solo lectura
    age = serializers.ReadOnlyField()
    antiguedad = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('age', 'antiguedad', 'is_admin')

class UserSerializer(serializers.ModelSerializer):
    # Campo de contraseña que solo se puede escribir
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        details = kwargs.pop("details", False)
        super(UserSerializer, self).__init__(*args, **kwargs)
        #  si es una intancia con detalles se habilita el campo profile
        if self.instance and details:
            profile = ProfileSerializer()
            # se agrega el campo profile al serializer
            self.fields["profile"] = profile

    # funcion para crear un nuevo usuario
    def create(self, validated_data):
        if not validated_data.get('first_name') or not validated_data.get('last_name'):
            raise serializers.ValidationError("First name and last name cannot be empty.")
        user = User.objects.create_user(
            username=validated_data['email'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']
        read_only_fields = ('age', 'antiguedad', 'is_admin')