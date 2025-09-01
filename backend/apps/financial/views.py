from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from django.utils import timezone
from apps.core.permissions import IsTenantUser
from .models import (
    Categoria, CentroCusto, ContaBancaria, LancamentoFinanceiro,
    Campanha, LancamentoCampanha, Orcamento, ItemOrcamento
)
from .serializers import (
    CategoriaSerializer, CentroCustoSerializer, ContaBancariaSerializer,
    LancamentoFinanceiroSerializer, CampanhaSerializer, LancamentoCampanhaSerializer,
    OrcamentoSerializer, ItemOrcamentoSerializer
)


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return Categoria.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)


class CentroCustoViewSet(viewsets.ModelViewSet):
    serializer_class = CentroCustoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['campus', 'responsavel']
    search_fields = ['nome', 'descricao', 'codigo']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return CentroCusto.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)


class ContaBancariaViewSet(viewsets.ModelViewSet):
    serializer_class = ContaBancariaSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_conta', 'ativa']
    search_fields = ['nome', 'banco', 'agencia', 'conta']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return ContaBancaria.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)


class LancamentoFinanceiroViewSet(viewsets.ModelViewSet):
    serializer_class = LancamentoFinanceiroSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'categoria', 'centro_custo', 'conta_bancaria', 'forma_pagamento', 'aprovado']
    search_fields = ['descricao', 'numero_documento', 'pessoa__nome_completo']
    ordering_fields = ['data_lancamento', 'valor', 'created_at']
    ordering = ['-data_lancamento']

    def get_queryset(self):
        return LancamentoFinanceiro.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja, responsavel=self.request.user)

    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        lancamento = self.get_object()
        lancamento.aprovado = True
        lancamento.aprovado_por = request.user
        lancamento.data_aprovacao = timezone.now()
        lancamento.save()
        
        serializer = self.get_serializer(lancamento)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def marcar_pago(self, request, pk=None):
        lancamento = self.get_object()
        lancamento.data_pagamento = request.data.get('data_pagamento', timezone.now().date())
        lancamento.save()
        
        serializer = self.get_serializer(lancamento)
        return Response(serializer.data)

    @action(detail=False)
    def resumo_financeiro(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset().filter(aprovado=True)
        
        if data_inicio:
            queryset = queryset.filter(data_lancamento__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_lancamento__lte=data_fim)
        
        entradas = queryset.filter(tipo='entrada').aggregate(
            total=Sum('valor'), count=Count('id')
        )
        saidas = queryset.filter(tipo='saida').aggregate(
            total=Sum('valor'), count=Count('id')
        )
        
        return Response({
            'entradas': {
                'total': entradas['total'] or 0,
                'quantidade': entradas['count'] or 0
            },
            'saidas': {
                'total': saidas['total'] or 0,
                'quantidade': saidas['count'] or 0
            },
            'saldo': (entradas['total'] or 0) - (saidas['total'] or 0)
        })

    @action(detail=False)
    def fluxo_caixa(self, request):
        ano = request.query_params.get('ano', timezone.now().year)
        
        meses = []
        for mes in range(1, 13):
            entradas = self.get_queryset().filter(
                tipo='entrada',
                aprovado=True,
                data_lancamento__year=ano,
                data_lancamento__month=mes
            ).aggregate(total=Sum('valor'))['total'] or 0
            
            saidas = self.get_queryset().filter(
                tipo='saida',
                aprovado=True,
                data_lancamento__year=ano,
                data_lancamento__month=mes
            ).aggregate(total=Sum('valor'))['total'] or 0
            
            meses.append({
                'mes': mes,
                'entradas': entradas,
                'saidas': saidas,
                'saldo': entradas - saidas
            })
        
        return Response({'ano': ano, 'meses': meses})


class CampanhaViewSet(viewsets.ModelViewSet):
    serializer_class = CampanhaSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['responsavel']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['data_inicio', 'meta_valor', 'created_at']
    ordering = ['-data_inicio']

    def get_queryset(self):
        return Campanha.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def adicionar_lancamento(self, request, pk=None):
        campanha = self.get_object()
        lancamento_id = request.data.get('lancamento_id')
        
        try:
            lancamento = LancamentoFinanceiro.objects.get(
                id=lancamento_id,
                igreja=self.request.user.igreja,
                tipo='entrada'
            )
            
            LancamentoCampanha.objects.get_or_create(
                campanha=campanha,
                lancamento=lancamento
            )
            
            return Response({'message': 'Lançamento adicionado à campanha'})
            
        except LancamentoFinanceiro.DoesNotExist:
            return Response({'error': 'Lançamento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False)
    def ativas(self, request):
        hoje = timezone.now().date()
        campanhas = self.get_queryset().filter(
            data_inicio__lte=hoje,
            data_fim__gte=hoje
        )
        
        serializer = self.get_serializer(campanhas, many=True)
        return Response(serializer.data)


class OrcamentoViewSet(viewsets.ModelViewSet):
    serializer_class = OrcamentoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ano', 'mes', 'campus', 'aprovado']
    search_fields = ['nome']
    ordering_fields = ['ano', 'mes', 'created_at']
    ordering = ['-ano', '-mes']

    def get_queryset(self):
        return Orcamento.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        orcamento = self.get_object()
        orcamento.aprovado = True
        orcamento.aprovado_por = request.user
        orcamento.data_aprovacao = timezone.now()
        orcamento.save()
        
        serializer = self.get_serializer(orcamento)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def adicionar_item(self, request, pk=None):
        orcamento = self.get_object()
        serializer = ItemOrcamentoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(orcamento=orcamento)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
