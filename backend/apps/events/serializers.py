from rest_framework import serializers
from .models import (
    Evento, InscricaoEvento, EscalaEvento, PresencaEvento, 
    CheckInEvento, RecursoEvento, ReservaRecurso
)


class EventoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.nome_completo', read_only=True)
    ministerio_nome = serializers.CharField(source='ministerio.nome', read_only=True)
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    total_inscricoes = serializers.ReadOnlyField()
    vagas_disponiveis = serializers.ReadOnlyField()
    
    class Meta:
        model = Evento
        fields = [
            'id', 'titulo', 'descricao', 'tipo', 'tipo_display', 'data_inicio', 'data_fim',
            'local', 'endereco', 'publico', 'requer_inscricao', 'limite_inscricoes',
            'valor_inscricao', 'responsavel', 'responsavel_nome', 'ministerio', 'ministerio_nome',
            'cor', 'imagem', 'observacoes', 'campus', 'campus_nome', 'total_inscricoes',
            'vagas_disponiveis', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class InscricaoEventoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    evento_titulo = serializers.CharField(source='evento.titulo', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = InscricaoEvento
        fields = [
            'id', 'evento', 'evento_titulo', 'pessoa', 'pessoa_nome', 'status', 'status_display',
            'data_inscricao', 'data_confirmacao', 'valor_pago', 'forma_pagamento', 'observacoes'
        ]
        read_only_fields = ['id', 'data_inscricao']


class EscalaEventoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    evento_titulo = serializers.CharField(source='evento.titulo', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = EscalaEvento
        fields = [
            'id', 'evento', 'evento_titulo', 'tipo', 'tipo_display', 'pessoa', 'pessoa_nome',
            'funcao', 'horario_inicio', 'horario_fim', 'confirmado', 'data_confirmacao', 'observacoes'
        ]


class PresencaEventoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    evento_titulo = serializers.CharField(source='evento.titulo', read_only=True)
    
    class Meta:
        model = PresencaEvento
        fields = [
            'id', 'evento', 'evento_titulo', 'pessoa', 'pessoa_nome', 'presente',
            'horario_chegada', 'horario_saida', 'visitante', 'primeira_visita', 'observacoes'
        ]


class CheckInEventoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    evento_titulo = serializers.CharField(source='evento.titulo', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel_checkin.nome_completo', read_only=True)
    
    class Meta:
        model = CheckInEvento
        fields = [
            'id', 'evento', 'evento_titulo', 'pessoa', 'pessoa_nome', 'codigo_qr',
            'data_checkin', 'responsavel_checkin', 'responsavel_nome', 'observacoes'
        ]
        read_only_fields = ['id', 'data_checkin']


class RecursoEventoSerializer(serializers.ModelSerializer):
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.nome_completo', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = RecursoEvento
        fields = [
            'id', 'nome', 'descricao', 'tipo', 'tipo_display', 'capacidade', 'localizacao',
            'disponivel', 'requer_aprovacao', 'responsavel', 'responsavel_nome',
            'campus', 'campus_nome', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class ReservaRecursoSerializer(serializers.ModelSerializer):
    recurso_nome = serializers.CharField(source='recurso.nome', read_only=True)
    evento_titulo = serializers.CharField(source='evento.titulo', read_only=True)
    solicitante_nome = serializers.CharField(source='solicitante.nome_completo', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.nome_completo', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ReservaRecurso
        fields = [
            'id', 'recurso', 'recurso_nome', 'evento', 'evento_titulo', 'data_inicio', 'data_fim',
            'solicitante', 'solicitante_nome', 'aprovado_por', 'aprovado_por_nome',
            'status', 'status_display', 'observacoes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
