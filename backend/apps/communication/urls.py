from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TemplateMensagemViewSet, ListaContatosViewSet, DisparoComunicacaoViewSet,
    ConfiguracaoEmailViewSet, ConfiguracaoWhatsAppViewSet, OptInOptOutViewSet,
    AutomacaoComunicacaoViewSet
)

router = DefaultRouter()
router.register(r'templates', TemplateMensagemViewSet, basename='template')
router.register(r'listas-contatos', ListaContatosViewSet, basename='lista-contatos')
router.register(r'disparos', DisparoComunicacaoViewSet, basename='disparo')
router.register(r'config-email', ConfiguracaoEmailViewSet, basename='config-email')
router.register(r'config-whatsapp', ConfiguracaoWhatsAppViewSet, basename='config-whatsapp')
router.register(r'preferencias', OptInOptOutViewSet, basename='preferencia')
router.register(r'automacoes', AutomacaoComunicacaoViewSet, basename='automacao')

urlpatterns = [
    path('', include(router.urls)),
]
