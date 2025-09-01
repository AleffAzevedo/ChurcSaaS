from django.contrib import admin
from .models import (
    Evento, InscricaoEvento, EscalaEvento, PresencaEvento,
    CheckInEvento, RecursoEvento, ReservaRecurso
)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'data_inicio', 'campus', 'responsavel', 'publico', 'is_active']
    list_filter = ['tipo', 'campus', 'publico', 'requer_inscricao', 'data_inicio']
    search_fields = ['titulo', 'descricao', 'local']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_inscricoes', 'vagas_disponiveis']


@admin.register(InscricaoEvento)
class InscricaoEventoAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'evento', 'status', 'data_inscricao', 'valor_pago']
    list_filter = ['status', 'evento', 'data_inscricao']
    search_fields = ['pessoa__nome_completo', 'evento__titulo']


@admin.register(EscalaEvento)
class EscalaEventoAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'evento', 'tipo', 'funcao', 'confirmado']
    list_filter = ['tipo', 'confirmado', 'evento']
    search_fields = ['pessoa__nome_completo', 'evento__titulo', 'funcao']


@admin.register(PresencaEvento)
class PresencaEventoAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'evento', 'presente', 'visitante', 'primeira_visita']
    list_filter = ['presente', 'visitante', 'primeira_visita', 'evento']
    search_fields = ['pessoa__nome_completo', 'evento__titulo']


@admin.register(CheckInEvento)
class CheckInEventoAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'evento', 'data_checkin', 'responsavel_checkin']
    list_filter = ['evento', 'data_checkin']
    search_fields = ['pessoa__nome_completo', 'evento__titulo', 'codigo_qr']
    readonly_fields = ['data_checkin']


@admin.register(RecursoEvento)
class RecursoEventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'campus', 'disponivel', 'requer_aprovacao', 'is_active']
    list_filter = ['tipo', 'campus', 'disponivel', 'requer_aprovacao']
    search_fields = ['nome', 'descricao', 'localizacao']


@admin.register(ReservaRecurso)
class ReservaRecursoAdmin(admin.ModelAdmin):
    list_display = ['recurso', 'evento', 'data_inicio', 'data_fim', 'status', 'solicitante']
    list_filter = ['status', 'recurso', 'data_inicio']
    search_fields = ['recurso__nome', 'evento__titulo', 'solicitante__nome_completo']
