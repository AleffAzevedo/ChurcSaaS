from rest_framework import serializers
from .models import (
    Categoria, CentroCusto, ContaBancaria, LancamentoFinanceiro,
    Campanha, LancamentoCampanha, Orcamento, ItemOrcamento
)


class CategoriaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'tipo', 'tipo_display', 'cor', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class CentroCustoSerializer(serializers.ModelSerializer):
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.nome_completo', read_only=True)
    
    class Meta:
        model = CentroCusto
        fields = [
            'id', 'nome', 'descricao', 'codigo', 'responsavel', 'responsavel_nome',
            'campus', 'campus_nome', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class ContaBancariaSerializer(serializers.ModelSerializer):
    tipo_conta_display = serializers.CharField(source='get_tipo_conta_display', read_only=True)
    saldo_atual = serializers.ReadOnlyField()
    
    class Meta:
        model = ContaBancaria
        fields = [
            'id', 'nome', 'banco', 'agencia', 'conta', 'tipo_conta', 'tipo_conta_display',
            'saldo_inicial', 'saldo_atual', 'ativa', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class LancamentoFinanceiroSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    forma_pagamento_display = serializers.CharField(source='get_forma_pagamento_display', read_only=True)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    centro_custo_nome = serializers.CharField(source='centro_custo.nome', read_only=True)
    conta_bancaria_nome = serializers.CharField(source='conta_bancaria.nome', read_only=True)
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.get_full_name', read_only=True)
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    status_pagamento = serializers.ReadOnlyField()
    
    class Meta:
        model = LancamentoFinanceiro
        fields = [
            'id', 'tipo', 'tipo_display', 'categoria', 'categoria_nome', 'centro_custo', 'centro_custo_nome',
            'conta_bancaria', 'conta_bancaria_nome', 'descricao', 'valor', 'data_lancamento',
            'data_vencimento', 'data_pagamento', 'forma_pagamento', 'forma_pagamento_display',
            'numero_documento', 'pessoa', 'pessoa_nome', 'responsavel', 'responsavel_nome',
            'observacoes', 'comprovante', 'aprovado', 'aprovado_por', 'aprovado_por_nome',
            'data_aprovacao', 'campus', 'campus_nome', 'status_pagamento',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class CampanhaSerializer(serializers.ModelSerializer):
    responsavel_nome = serializers.CharField(source='responsavel.nome_completo', read_only=True)
    valor_arrecadado = serializers.ReadOnlyField()
    percentual_meta = serializers.ReadOnlyField()
    
    class Meta:
        model = Campanha
        fields = [
            'id', 'nome', 'descricao', 'meta_valor', 'data_inicio', 'data_fim',
            'responsavel', 'responsavel_nome', 'imagem', 'cor', 'valor_arrecadado',
            'percentual_meta', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class LancamentoCampanhaSerializer(serializers.ModelSerializer):
    campanha_nome = serializers.CharField(source='campanha.nome', read_only=True)
    lancamento_descricao = serializers.CharField(source='lancamento.descricao', read_only=True)
    lancamento_valor = serializers.DecimalField(source='lancamento.valor', max_digits=15, decimal_places=2, read_only=True)
    
    class Meta:
        model = LancamentoCampanha
        fields = ['id', 'campanha', 'campanha_nome', 'lancamento', 'lancamento_descricao', 'lancamento_valor']


class ItemOrcamentoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    centro_custo_nome = serializers.CharField(source='centro_custo.nome', read_only=True)
    valor_realizado = serializers.ReadOnlyField()
    
    class Meta:
        model = ItemOrcamento
        fields = [
            'id', 'categoria', 'categoria_nome', 'centro_custo', 'centro_custo_nome',
            'descricao', 'valor_previsto', 'valor_realizado', 'observacoes'
        ]


class OrcamentoSerializer(serializers.ModelSerializer):
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    aprovado_por_nome = serializers.CharField(source='aprovado_por.get_full_name', read_only=True)
    itens = ItemOrcamentoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Orcamento
        fields = [
            'id', 'nome', 'ano', 'mes', 'valor_previsto_entrada', 'valor_previsto_saida',
            'aprovado', 'aprovado_por', 'aprovado_por_nome', 'data_aprovacao',
            'campus', 'campus_nome', 'itens', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
