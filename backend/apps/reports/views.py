from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from apps.core.permissions import IsTenantUser
from .models import RelatorioPersonalizado, ExecucaoRelatorio, Dashboard, Widget
from .serializers import (
    RelatorioPersonalizadoSerializer, ExecucaoRelatorioSerializer,
    DashboardSerializer, WidgetSerializer
)


class RelatorioPersonalizadoViewSet(viewsets.ModelViewSet):
    serializer_class = RelatorioPersonalizadoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'publico', 'criado_por']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return RelatorioPersonalizado.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja, criado_por=self.request.user)

    @action(detail=True, methods=['post'])
    def executar(self, request, pk=None):
        relatorio = self.get_object()
        parametros = request.data.get('parametros', {})
        
        execucao = ExecucaoRelatorio.objects.create(
            relatorio=relatorio,
            usuario=request.user,
            parametros_utilizados=parametros,
            status='executando'
        )
        
        return Response({
            'execucao_id': execucao.id,
            'message': 'Relatório em execução'
        }, status=status.HTTP_202_ACCEPTED)


class ExecucaoRelatorioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExecucaoRelatorioSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['relatorio', 'usuario', 'status']
    search_fields = ['relatorio__nome']
    ordering_fields = ['data_execucao']
    ordering = ['-data_execucao']

    def get_queryset(self):
        return ExecucaoRelatorio.objects.filter(relatorio__igreja=self.request.user.igreja)


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publico', 'padrao', 'criado_por']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return Dashboard.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja, criado_por=self.request.user)

    @action(detail=True, methods=['post'])
    def adicionar_widget(self, request, pk=None):
        dashboard = self.get_object()
        serializer = WidgetSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(dashboard=dashboard)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def dashboard_principal(self, request):
        try:
            dashboard = self.get_queryset().filter(padrao=True).first()
            if not dashboard:
                dashboard = self.get_queryset().first()
            
            if dashboard:
                serializer = self.get_serializer(dashboard)
                return Response(serializer.data)
            else:
                return Response({'message': 'Nenhum dashboard encontrado'}, 
                              status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False)
    def estatisticas_gerais(self, request):
        from apps.members.models import Pessoa
        from apps.groups.models import Grupo
        from apps.events.models import Evento
        from apps.financial.models import LancamentoFinanceiro
        
        igreja = request.user.igreja
        
        total_membros = Pessoa.objects.filter(igreja=igreja, is_active=True).count()
        total_grupos = Grupo.objects.filter(igreja=igreja, is_active=True).count()
        
        hoje = timezone.now().date()
        eventos_mes = Evento.objects.filter(
            igreja=igreja,
            data_inicio__year=hoje.year,
            data_inicio__month=hoje.month
        ).count()
        
        entradas_mes = LancamentoFinanceiro.objects.filter(
            igreja=igreja,
            tipo='entrada',
            data_lancamento__year=hoje.year,
            data_lancamento__month=hoje.month,
            aprovado=True
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        saidas_mes = LancamentoFinanceiro.objects.filter(
            igreja=igreja,
            tipo='saida',
            data_lancamento__year=hoje.year,
            data_lancamento__month=hoje.month,
            aprovado=True
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        return Response({
            'membros': {
                'total': total_membros,
                'novos_mes': Pessoa.objects.filter(
                    igreja=igreja,
                    created_at__year=hoje.year,
                    created_at__month=hoje.month
                ).count()
            },
            'grupos': {
                'total': total_grupos,
                'media_membros': Grupo.objects.filter(
                    igreja=igreja, is_active=True
                ).aggregate(media=Avg('membrogrupo__id'))['media'] or 0
            },
            'eventos': {
                'mes_atual': eventos_mes,
                'proximos': Evento.objects.filter(
                    igreja=igreja,
                    data_inicio__gte=timezone.now()
                ).count()
            },
            'financeiro': {
                'entradas_mes': float(entradas_mes),
                'saidas_mes': float(saidas_mes),
                'saldo_mes': float(entradas_mes - saidas_mes)
            }
        })


class WidgetViewSet(viewsets.ModelViewSet):
    serializer_class = WidgetSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dashboard', 'tipo']
    search_fields = ['nome']
    ordering_fields = ['posicao_y', 'posicao_x']
    ordering = ['posicao_y', 'posicao_x']

    def get_queryset(self):
        return Widget.objects.filter(dashboard__igreja=self.request.user.igreja)

    @action(detail=True, methods=['get'])
    def dados(self, request, pk=None):
        widget = self.get_object()
        
        return Response({
            'dados': [],
            'message': 'Dados do widget não implementados'
        })
