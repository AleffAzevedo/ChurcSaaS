from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PessoaViewSet, FamiliaViewSet, MinisterioViewSet, PedidoOracaoViewSet, VisitaViewSet

router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet, basename='pessoa')
router.register(r'familias', FamiliaViewSet, basename='familia')
router.register(r'ministerios', MinisterioViewSet, basename='ministerio')
router.register(r'pedidos-oracao', PedidoOracaoViewSet, basename='pedido-oracao')
router.register(r'visitas', VisitaViewSet, basename='visita')

urlpatterns = [
    path('', include(router.urls)),
]
