from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AjustesViewSet

router = DefaultRouter()
router.register(r'ajustes', AjustesViewSet, basename='ajustes')

urlpatterns = [
    path('', include(router.urls)),
]
