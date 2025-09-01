from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, CentroCustoViewSet, ContaBancariaViewSet,
    LancamentoFinanceiroViewSet, CampanhaViewSet, OrcamentoViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'centros-custo', CentroCustoViewSet, basename='centro-custo')
router.register(r'contas-bancarias', ContaBancariaViewSet, basename='conta-bancaria')
router.register(r'lancamentos', LancamentoFinanceiroViewSet, basename='lancamento')
router.register(r'campanhas', CampanhaViewSet, basename='campanha')
router.register(r'orcamentos', OrcamentoViewSet, basename='orcamento')

urlpatterns = [
    path('', include(router.urls)),
]
