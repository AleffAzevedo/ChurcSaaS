from django.contrib import admin
from .models import Pessoa, Familia, MembroFamilia, Ministerio, MembroMinisterio, PedidoOracao, Visita


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'status_membro', 'campus', 'telefone', 'email', 'is_active']
    list_filter = ['status_membro', 'campus', 'sexo', 'estado_civil', 'is_active']
    search_fields = ['nome_completo', 'nome_preferencia', 'cpf', 'email', 'telefone']
    readonly_fields = ['id', 'created_at', 'updated_at', 'idade']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_completo', 'nome_preferencia', 'cpf', 'rg', 'data_nascimento', 'idade')
        }),
        ('Informações Pessoais', {
            'fields': ('sexo', 'estado_civil', 'profissao', 'escolaridade')
        }),
        ('Contato', {
            'fields': ('telefone', 'celular', 'email')
        }),
        ('Endereço', {
            'fields': ('endereco', 'cep', 'cidade', 'estado')
        }),
        ('Igreja', {
            'fields': ('igreja', 'campus', 'status_membro')
        }),
        ('Datas Importantes', {
            'fields': ('data_primeira_visita', 'data_conversao', 'data_batismo', 'data_membresia')
        }),
        ('Outros', {
            'fields': ('foto', 'observacoes', 'aceite_lgpd', 'is_active')
        }),
    )


@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'igreja', 'campus', 'cidade', 'is_active']
    list_filter = ['campus', 'cidade', 'is_active']
    search_fields = ['nome', 'cidade']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(MembroFamilia)
class MembroFamiliaAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'familia', 'parentesco', 'responsavel_financeiro']
    list_filter = ['parentesco', 'responsavel_financeiro']
    search_fields = ['pessoa__nome_completo', 'familia__nome']


@admin.register(Ministerio)
class MinisterioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'igreja', 'campus', 'lider', 'is_active']
    list_filter = ['campus', 'is_active']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(MembroMinisterio)
class MembroMinisterioAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'ministerio', 'funcao', 'data_inicio', 'data_fim']
    list_filter = ['funcao', 'ministerio', 'data_inicio']
    search_fields = ['pessoa__nome_completo', 'ministerio__nome']


@admin.register(PedidoOracao)
class PedidoOracaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'pessoa', 'publico', 'urgente', 'data_resposta', 'created_at']
    list_filter = ['publico', 'urgente', 'data_resposta', 'created_at']
    search_fields = ['titulo', 'descricao', 'pessoa__nome_completo']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'tipo_visita', 'data_visita', 'visitante', 'proxima_visita']
    list_filter = ['tipo_visita', 'data_visita', 'visitante']
    search_fields = ['pessoa__nome_completo', 'motivo', 'observacoes']
    readonly_fields = ['id', 'created_at', 'updated_at']
