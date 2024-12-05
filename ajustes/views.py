from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)