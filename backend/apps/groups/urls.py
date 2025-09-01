from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GrupoViewSet, ReuniaoViewSet, MaterialEstudoViewSet

router = DefaultRouter()
router.register(r'grupos', GrupoViewSet, basename='grupo')
router.register(r'reunioes', ReuniaoViewSet, basename='reuniao')
router.register(r'materiais', MaterialEstudoViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
]
