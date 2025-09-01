from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from apps.core.permissions import IsTenantUser
from .models import Grupo, MembroGrupo, Reuniao, PresencaReuniao, MaterialEstudo, GrupoMaterial
from .serializers import (
    GrupoSerializer, MembroGrupoSerializer, ReuniaoSerializer, PresencaReuniaoSerializer,
    MaterialEstudoSerializer, GrupoMaterialSerializer
)


class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'campus', 'lider']
    search_fields = ['nome', 'descricao', 'endereco']
    ordering_fields = ['nome', 'created_at', 'total_membros']
    ordering = ['nome']

    def get_queryset(self):
        return Grupo.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def adicionar_membro(self, request, pk=None):
        grupo = self.get_object()
        serializer = MembroGrupoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(grupo=grupo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remover_membro(self, request, pk=None):
        grupo = self.get_object()
        pessoa_id = request.data.get('pessoa_id')
        try:
            membro = MembroGrupo.objects.get(grupo=grupo, pessoa_id=pessoa_id)
            membro.data_saida = request.data.get('data_saida')
            membro.save()
            return Response({'message': 'Membro removido do grupo'})
        except MembroGrupo.DoesNotExist:
            return Response({'error': 'Membro não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        grupo = self.get_object()
        
        reunioes = grupo.reunioes.all()
        total_reunioes = reunioes.count()
        
        if total_reunioes > 0:
            media_presentes = reunioes.aggregate(Avg('total_presentes'))['total_presentes__avg'] or 0
            media_visitantes = reunioes.aggregate(Avg('total_visitantes'))['total_visitantes__avg'] or 0
            total_conversoes = sum(r.total_conversoes for r in reunioes)
        else:
            media_presentes = 0
            media_visitantes = 0
            total_conversoes = 0
        
        return Response({
            'total_membros': grupo.total_membros,
            'meta_membros': grupo.meta_membros,
            'percentual_meta': grupo.percentual_meta,
            'total_reunioes': total_reunioes,
            'media_presentes': round(media_presentes, 1),
            'media_visitantes': round(media_visitantes, 1),
            'total_conversoes': total_conversoes,
        })

    @action(detail=False)
    def dashboard(self, request):
        grupos = self.get_queryset()
        
        total_grupos = grupos.count()
        total_membros = sum(g.total_membros for g in grupos)
        grupos_acima_meta = grupos.filter(membrogrupo__data_saida__isnull=True).annotate(
            total=Count('membrogrupo')
        ).filter(total__gte=models.F('meta_membros')).count()
        
        return Response({
            'total_grupos': total_grupos,
            'total_membros': total_membros,
            'grupos_acima_meta': grupos_acima_meta,
            'percentual_acima_meta': (grupos_acima_meta / total_grupos * 100) if total_grupos > 0 else 0,
        })


class ReuniaoViewSet(viewsets.ModelViewSet):
    serializer_class = ReuniaoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grupo', 'responsavel']
    search_fields = ['tema', 'versiculo', 'resumo']
    ordering_fields = ['data_reuniao', 'created_at']
    ordering = ['-data_reuniao']

    def get_queryset(self):
        return Reuniao.objects.filter(grupo__igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def registrar_presenca(self, request, pk=None):
        reuniao = self.get_object()
        presencas_data = request.data.get('presencas', [])
        
        for presenca_data in presencas_data:
            pessoa_id = presenca_data.get('pessoa_id')
            presente = presenca_data.get('presente', True)
            visitante = presenca_data.get('visitante', False)
            
            PresencaReuniao.objects.update_or_create(
                reuniao=reuniao,
                pessoa_id=pessoa_id,
                defaults={
                    'presente': presente,
                    'visitante': visitante,
                    'observacoes': presenca_data.get('observacoes', '')
                }
            )
        
        reuniao.total_presentes = reuniao.presencas.filter(presente=True).count()
        reuniao.total_visitantes = reuniao.presencas.filter(visitante=True).count()
        reuniao.save()
        
        return Response({'message': 'Presenças registradas com sucesso'})

    @action(detail=False)
    def relatorio_frequencia(self, request):
        grupo_id = request.query_params.get('grupo_id')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = self.get_queryset()
        
        if grupo_id:
            queryset = queryset.filter(grupo_id=grupo_id)
        if data_inicio:
            queryset = queryset.filter(data_reuniao__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_reuniao__lte=data_fim)
        
        reunioes = queryset.order_by('-data_reuniao')
        serializer = self.get_serializer(reunioes, many=True)
        
        return Response({
            'reunioes': serializer.data,
            'total_reunioes': reunioes.count(),
            'media_presentes': reunioes.aggregate(Avg('total_presentes'))['total_presentes__avg'] or 0,
        })


class MaterialEstudoViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialEstudoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria']
    search_fields = ['titulo', 'descricao', 'autor']
    ordering_fields = ['titulo', 'data_publicacao', 'created_at']
    ordering = ['-data_publicacao', 'titulo']

    def get_queryset(self):
        return MaterialEstudo.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def associar_grupo(self, request, pk=None):
        material = self.get_object()
        grupo_id = request.data.get('grupo_id')
        data_inicio = request.data.get('data_inicio')
        
        try:
            grupo = Grupo.objects.get(id=grupo_id, igreja=self.request.user.igreja)
            GrupoMaterial.objects.create(
                grupo=grupo,
                material=material,
                data_inicio=data_inicio,
                observacoes=request.data.get('observacoes', '')
            )
            return Response({'message': 'Material associado ao grupo com sucesso'})
        except Grupo.DoesNotExist:
            return Response({'error': 'Grupo não encontrado'}, status=status.HTTP_404_NOT_FOUND)
