from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Ajustes
from .serializers import AjustesSerializer, AjustesUpdateSerializer

class AjustesViewSet(viewsets.ModelViewSet):
    queryset = Ajustes.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return AjustesUpdateSerializer
        return AjustesSerializer