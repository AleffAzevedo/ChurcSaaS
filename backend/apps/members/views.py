from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsTenantUser
from .models import Pessoa, Familia, MembroFamilia, Ministerio, MembroMinisterio, PedidoOracao, Visita
from .serializers import (
    PessoaSerializer, FamiliaSerializer, MembroFamiliaSerializer,
    MinisterioSerializer, MembroMinisterioSerializer, PedidoOracaoSerializer, VisitaSerializer
)


class PessoaViewSet(viewsets.ModelViewSet):
    serializer_class = PessoaSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status_membro', 'campus', 'sexo', 'estado_civil']
    search_fields = ['nome_completo', 'nome_preferencia', 'cpf', 'email', 'telefone', 'celular']
    ordering_fields = ['nome_completo', 'data_nascimento', 'created_at']
    ordering = ['nome_completo']

    def get_queryset(self):
        return Pessoa.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def converter_membro(self, request, pk=None):
        pessoa = self.get_object()
        pessoa.status_membro = 'membro'
        pessoa.data_membresia = request.data.get('data_membresia')
        pessoa.save()
        return Response({'message': 'Pessoa convertida para membro com sucesso'})

    @action(detail=True, methods=['post'])
    def registrar_batismo(self, request, pk=None):
        pessoa = self.get_object()
        pessoa.data_batismo = request.data.get('data_batismo')
        pessoa.save()
        return Response({'message': 'Batismo registrado com sucesso'})

    @action(detail=False)
    def aniversariantes(self, request):
        from datetime import date
        hoje = date.today()
        mes = request.query_params.get('mes', hoje.month)
        
        aniversariantes = self.get_queryset().filter(
            data_nascimento__month=mes,
            is_active=True
        ).order_by('data_nascimento__day')
        
        serializer = self.get_serializer(aniversariantes, many=True)
        return Response(serializer.data)


class FamiliaViewSet(viewsets.ModelViewSet):
    serializer_class = FamiliaSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['campus']
    search_fields = ['nome', 'cidade']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return Familia.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def adicionar_membro(self, request, pk=None):
        familia = self.get_object()
        serializer = MembroFamiliaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(familia=familia)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remover_membro(self, request, pk=None):
        familia = self.get_object()
        pessoa_id = request.data.get('pessoa_id')
        try:
            membro = MembroFamilia.objects.get(familia=familia, pessoa_id=pessoa_id)
            membro.delete()
            return Response({'message': 'Membro removido da família'})
        except MembroFamilia.DoesNotExist:
            return Response({'error': 'Membro não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class MinisterioViewSet(viewsets.ModelViewSet):
    serializer_class = MinisterioSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['campus']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return Ministerio.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def adicionar_membro(self, request, pk=None):
        ministerio = self.get_object()
        serializer = MembroMinisterioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ministerio=ministerio)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def atualizar_membro(self, request, pk=None):
        ministerio = self.get_object()
        membro_id = request.data.get('membro_id')
        try:
            membro = MembroMinisterio.objects.get(id=membro_id, ministerio=ministerio)
            serializer = MembroMinisterioSerializer(membro, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MembroMinisterio.DoesNotExist:
            return Response({'error': 'Membro não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class PedidoOracaoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoOracaoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publico', 'urgente', 'pessoa']
    search_fields = ['titulo', 'descricao', 'pessoa__nome_completo']
    ordering_fields = ['created_at', 'urgente']
    ordering = ['-urgente', '-created_at']

    def get_queryset(self):
        return PedidoOracao.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja, responsavel=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_respondido(self, request, pk=None):
        pedido = self.get_object()
        pedido.data_resposta = request.data.get('data_resposta')
        pedido.testemunho = request.data.get('testemunho', '')
        pedido.save()
        return Response({'message': 'Pedido marcado como respondido'})


class VisitaViewSet(viewsets.ModelViewSet):
    serializer_class = VisitaSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_visita', 'pessoa', 'visitante']
    search_fields = ['pessoa__nome_completo', 'motivo', 'observacoes']
    ordering_fields = ['data_visita', 'created_at']
    ordering = ['-data_visita']

    def get_queryset(self):
        return Visita.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja, visitante=self.request.user)
