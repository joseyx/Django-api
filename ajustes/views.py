from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from .models import Ajustes, Archivo
from .serializers import AjustesSerializer, AjustesUpdateSerializer, ArchivoSerializer


class AjustesViewSet(viewsets.ModelViewSet):
    queryset = Ajustes.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return AjustesUpdateSerializer
        return AjustesSerializer

class ArchivosViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ArchivoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo_de_archivo=tipo)  # Adjust `tipo` to match your model field
        return queryset