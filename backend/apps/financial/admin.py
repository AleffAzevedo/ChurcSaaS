from django.contrib import admin
from .models import (
    Categoria, CentroCusto, ContaBancaria, LancamentoFinanceiro,
    Campanha, LancamentoCampanha, Orcamento, ItemOrcamento
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'igreja', 'is_active']
    list_filter = ['tipo', 'igreja', 'is_active']
    search_fields = ['nome', 'descricao']


@admin.register(CentroCusto)
class CentroCustoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'igreja', 'campus', 'responsavel', 'is_active']
    list_filter = ['igreja', 'campus', 'is_active']
    search_fields = ['nome', 'codigo', 'descricao']


@admin.register(ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'banco', 'tipo_conta', 'saldo_atual', 'ativa', 'is_active']
    list_filter = ['tipo_conta', 'ativa', 'is_active']
    search_fields = ['nome', 'banco', 'agencia', 'conta']
    readonly_fields = ['saldo_atual']


@admin.register(LancamentoFinanceiro)
class LancamentoFinanceiroAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'tipo', 'valor', 'data_lancamento', 'aprovado', 'status_pagamento']
    list_filter = ['tipo', 'categoria', 'aprovado', 'forma_pagamento', 'data_lancamento']
    search_fields = ['descricao', 'numero_documento', 'pessoa__nome_completo']
    readonly_fields = ['status_pagamento']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'categoria', 'descricao', 'valor')
        }),
        ('Datas', {
            'fields': ('data_lancamento', 'data_vencimento', 'data_pagamento')
        }),
        ('Pagamento', {
            'fields': ('forma_pagamento', 'numero_documento', 'conta_bancaria')
        }),
        ('Organização', {
            'fields': ('centro_custo', 'campus', 'pessoa')
        }),
        ('Aprovação', {
            'fields': ('aprovado', 'aprovado_por', 'data_aprovacao')
        }),
        ('Outros', {
            'fields': ('observacoes', 'comprovante')
        }),
    )


@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'meta_valor', 'valor_arrecadado', 'percentual_meta', 'data_inicio', 'data_fim']
    list_filter = ['data_inicio', 'data_fim', 'responsavel']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['valor_arrecadado', 'percentual_meta']


@admin.register(LancamentoCampanha)
class LancamentoCampanhaAdmin(admin.ModelAdmin):
    list_display = ['campanha', 'lancamento', 'lancamento_valor']
    list_filter = ['campanha']
    search_fields = ['campanha__nome', 'lancamento__descricao']
    
    def lancamento_valor(self, obj):
        return f"R$ {obj.lancamento.valor}"
    lancamento_valor.short_description = 'Valor'


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ano', 'mes', 'valor_previsto_entrada', 'valor_previsto_saida', 'aprovado']
    list_filter = ['ano', 'mes', 'aprovado', 'campus']
    search_fields = ['nome']


@admin.register(ItemOrcamento)
class ItemOrcamentoAdmin(admin.ModelAdmin):
    list_display = ['orcamento', 'categoria', 'descricao', 'valor_previsto', 'valor_realizado']
    list_filter = ['orcamento', 'categoria']
    search_fields = ['descricao', 'orcamento__nome']
    readonly_fields = ['valor_realizado']
