from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Modelo de usuario personalizado que extiende AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

# Modelo de perfil asociado a cada usuario
class Profile(models.Model):
    # Validador para el número de teléfono
    phone_regex = RegexValidator(
        regex=r'^\+58\d{10}$',
        message="El número de teléfono debe estar en el formato: '+584241234567'."
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Campos relacionados con el rol del usuario
    rol = models.CharField(max_length=10, default='user', choices=[('user', 'user'), ('admin', 'admin')])
    # Campos personales
    genero = models.CharField(max_length=10, default='', choices=[('masculino', 'masculino'), ('femenino', 'femenino'), ('', ''), ('user', 'user')])
    # Campos de dirección
    pais = models.CharField(max_length=30, blank=True)
    estado = models.CharField(max_length=30, blank=True)
    ciudad = models.CharField(max_length=30, blank=True)
    codigo_postal = models.CharField(max_length=30, blank=True)
    # Campos de coordenadas
    latitud = models.FloatField(default=0)
    longitud = models.FloatField(default=0)
    # Campos de perfil
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    numero_telefono = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    identificacion = models.CharField(max_length=30, blank=True)
    # Campos de imagen
    imagen_perfil = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    imagen_perfil_big = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    imagen_perfil_medium = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    imagen_perfil_mini = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    # Ruta de la imagen por defecto
    DEFAULT_IMAGE_PATH = 'profile_images/placeholder.png'

    # Propiedad para verificar si el usuario es administrador
    @property
    def is_admin(self):
        return self.rol == 'admin'

    # Propiedad para calcular la edad del usuario
    @property
    def age(self):
        if self.fecha_nacimiento is None:
            return None
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
                    (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    # Propiedad para calcular la antigüedad del usuario en días
    @property
    def antiguedad(self):
        if self.fecha_registro is None:
            return None
        today = date.today()
        return (today - self.fecha_registro).days

    # Función para representar el perfil como una cadena
    def __str__(self):
        return self.user.email