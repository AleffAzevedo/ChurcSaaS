from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from apps.core.permissions import IsTenantUser
from .models import (
    Evento, InscricaoEvento, EscalaEvento, PresencaEvento,
    CheckInEvento, RecursoEvento, ReservaRecurso
)
from .serializers import (
    EventoSerializer, InscricaoEventoSerializer, EscalaEventoSerializer,
    PresencaEventoSerializer, CheckInEventoSerializer, RecursoEventoSerializer,
    ReservaRecursoSerializer
)


class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'campus', 'responsavel', 'ministerio', 'publico']
    search_fields = ['titulo', 'descricao', 'local']
    ordering_fields = ['data_inicio', 'created_at']
    ordering = ['data_inicio']

    def get_queryset(self):
        return Evento.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=False)
    def proximos(self, request):
        agora = timezone.now()
        eventos = self.get_queryset().filter(
            data_inicio__gte=agora,
            publico=True
        ).order_by('data_inicio')[:10]
        
        serializer = self.get_serializer(eventos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def inscrever(self, request, pk=None):
        evento = self.get_object()
        pessoa_id = request.data.get('pessoa_id')
        
        if evento.limite_inscricoes and evento.total_inscricoes >= evento.limite_inscricoes:
            return Response({'error': 'Evento lotado'}, status=status.HTTP_400_BAD_REQUEST)
        
        inscricao, created = InscricaoEvento.objects.get_or_create(
            evento=evento,
            pessoa_id=pessoa_id,
            defaults={
                'status': 'confirmada' if not evento.requer_inscricao else 'pendente',
                'data_confirmacao': timezone.now() if not evento.requer_inscricao else None
            }
        )
        
        if not created:
            return Response({'error': 'Pessoa já inscrita'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = InscricaoEventoSerializer(inscricao)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def checkin(self, request, pk=None):
        evento = self.get_object()
        pessoa_id = request.data.get('pessoa_id')
        codigo_qr = request.data.get('codigo_qr', '')
        
        checkin, created = CheckInEvento.objects.get_or_create(
            evento=evento,
            pessoa_id=pessoa_id,
            defaults={
                'codigo_qr': codigo_qr,
                'responsavel_checkin': request.user.pessoa if hasattr(request.user, 'pessoa') else None
            }
        )
        
        PresencaEvento.objects.update_or_create(
            evento=evento,
            pessoa_id=pessoa_id,
            defaults={
                'presente': True,
                'horario_chegada': timezone.now(),
                'visitante': request.data.get('visitante', False),
                'primeira_visita': request.data.get('primeira_visita', False)
            }
        )
        
        serializer = CheckInEventoSerializer(checkin)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class InscricaoEventoViewSet(viewsets.ModelViewSet):
    serializer_class = InscricaoEventoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['evento', 'pessoa', 'status']
    search_fields = ['pessoa__nome_completo', 'evento__titulo']
    ordering_fields = ['data_inscricao', 'data_confirmacao']
    ordering = ['-data_inscricao']

    def get_queryset(self):
        return InscricaoEvento.objects.filter(evento__igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        inscricao = self.get_object()
        inscricao.status = 'confirmada'
        inscricao.data_confirmacao = timezone.now()
        inscricao.save()
        
        serializer = self.get_serializer(inscricao)
        return Response(serializer.data)


class EscalaEventoViewSet(viewsets.ModelViewSet):
    serializer_class = EscalaEventoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['evento', 'tipo', 'pessoa', 'confirmado']
    search_fields = ['pessoa__nome_completo', 'evento__titulo', 'funcao']
    ordering_fields = ['evento__data_inicio', 'tipo']
    ordering = ['evento__data_inicio', 'tipo']

    def get_queryset(self):
        return EscalaEvento.objects.filter(evento__igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        escala = self.get_object()
        escala.confirmado = True
        escala.data_confirmacao = timezone.now()
        escala.save()
        
        serializer = self.get_serializer(escala)
        return Response(serializer.data)


class RecursoEventoViewSet(viewsets.ModelViewSet):
    serializer_class = RecursoEventoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'campus', 'disponivel', 'requer_aprovacao']
    search_fields = ['nome', 'descricao', 'localizacao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return RecursoEvento.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def reservar(self, request, pk=None):
        recurso = self.get_object()
        evento_id = request.data.get('evento_id')
        data_inicio = request.data.get('data_inicio')
        data_fim = request.data.get('data_fim')
        
        try:
            evento = Evento.objects.get(id=evento_id, igreja=self.request.user.igreja)
            
            reserva = ReservaRecurso.objects.create(
                recurso=recurso,
                evento=evento,
                data_inicio=data_inicio,
                data_fim=data_fim,
                solicitante=request.user.pessoa if hasattr(request.user, 'pessoa') else None,
                status='aprovada' if not recurso.requer_aprovacao else 'pendente'
            )
            
            serializer = ReservaRecursoSerializer(reserva)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Evento.DoesNotExist:
            return Response({'error': 'Evento não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ReservaRecursoViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaRecursoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['recurso', 'evento', 'status', 'solicitante']
    search_fields = ['recurso__nome', 'evento__titulo', 'solicitante__nome_completo']
    ordering_fields = ['data_inicio', 'created_at']
    ordering = ['data_inicio']

    def get_queryset(self):
        return ReservaRecurso.objects.filter(recurso__igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        reserva = self.get_object()
        reserva.status = 'aprovada'
        reserva.aprovado_por = request.user.pessoa if hasattr(request.user, 'pessoa') else None
        reserva.save()
        
        serializer = self.get_serializer(reserva)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rejeitar(self, request, pk=None):
        reserva = self.get_object()
        reserva.status = 'rejeitada'
        reserva.observacoes = request.data.get('motivo', reserva.observacoes)
        reserva.save()
        
        serializer = self.get_serializer(reserva)
        return Response(serializer.data)
