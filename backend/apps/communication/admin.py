from django.contrib import admin
from .models import (
    TemplateMensagem, ListaContatos, ContatoLista, DisparoComunicacao,
    LogEnvioMensagem, ConfiguracaoEmail, ConfiguracaoWhatsApp,
    OptInOptOut, AutomacaoComunicacao
)


@admin.register(TemplateMensagem)
class TemplateMensagemAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'categoria', 'ativo', 'is_active']
    list_filter = ['tipo', 'categoria', 'ativo', 'is_active']
    search_fields = ['nome', 'assunto', 'conteudo']


@admin.register(ListaContatos)
class ListaContatosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'total_contatos', 'is_active']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['total_contatos']


@admin.register(ContatoLista)
class ContatoListaAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'lista', 'data_adicao', 'ativo']
    list_filter = ['lista', 'ativo', 'data_adicao']
    search_fields = ['pessoa__nome_completo', 'lista__nome']


@admin.register(DisparoComunicacao)
class DisparoComunicacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'status', 'total_destinatarios', 'total_enviados', 'taxa_entrega']
    list_filter = ['tipo', 'status', 'created_at']
    search_fields = ['titulo', 'assunto']
    readonly_fields = ['taxa_entrega', 'taxa_leitura']


@admin.register(LogEnvioMensagem)
class LogEnvioMensagemAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'disparo', 'destinatario', 'status', 'data_envio', 'tentativas']
    list_filter = ['status', 'disparo', 'data_envio']
    search_fields = ['pessoa__nome_completo', 'destinatario', 'disparo__titulo']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ConfiguracaoEmail)
class ConfiguracaoEmailAdmin(admin.ModelAdmin):
    list_display = ['nome_remetente', 'email_remetente', 'servidor_smtp', 'ativo', 'is_active']
    list_filter = ['ativo', 'usar_tls', 'is_active']
    search_fields = ['nome_remetente', 'email_remetente']


@admin.register(ConfiguracaoWhatsApp)
class ConfiguracaoWhatsAppAdmin(admin.ModelAdmin):
    list_display = ['numero_telefone', 'provedor', 'ativo', 'is_active']
    list_filter = ['provedor', 'ativo', 'is_active']
    search_fields = ['numero_telefone']


@admin.register(OptInOptOut)
class OptInOptOutAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'aceita_email', 'aceita_sms', 'aceita_whatsapp', 'data_opt_in']
    list_filter = ['aceita_email', 'aceita_sms', 'aceita_whatsapp', 'aceita_push']
    search_fields = ['pessoa__nome_completo']


@admin.register(AutomacaoComunicacao)
class AutomacaoComunicacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'trigger', 'template', 'ativo', 'ultima_execucao']
    list_filter = ['trigger', 'ativo', 'template']
    search_fields = ['nome', 'descricao']
