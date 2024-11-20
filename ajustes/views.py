from rest_framework import viewsets
from rest_framework.decorators import action
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

    @action(detail=False, methods=['get'])
    def get_imagenes(self, request):
        queryset = Archivo.objects.filter(tipo_de_archivo='imagen')
        serializer = ArchivoSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_documentos(self, request):
        queryset = Archivo.objects.filter(tipo_de_archivo='documento')
        serializer = ArchivoSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_audios(self, request):
        queryset = Archivo.objects.filter(tipo_de_archivo='audio')
        serializer = ArchivoSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_videos(self, request):
        queryset = Archivo.objects.filter(tipo_de_archivo='video')
        serializer = ArchivoSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_subtitulos(self, request):
        queryset = Archivo.objects.filter(tipo_de_archivo='subtitulo')
        serializer = ArchivoSerializer(queryset, many=True)
        return Response(serializer.data)
