from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventoViewSet, InscricaoEventoViewSet, EscalaEventoViewSet,
    RecursoEventoViewSet, ReservaRecursoViewSet
)

router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')
router.register(r'inscricoes', InscricaoEventoViewSet, basename='inscricao')
router.register(r'escalas', EscalaEventoViewSet, basename='escala')
router.register(r'recursos', RecursoEventoViewSet, basename='recurso')
router.register(r'reservas', ReservaRecursoViewSet, basename='reserva')

urlpatterns = [
    path('', include(router.urls)),
]
