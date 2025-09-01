from rest_framework import serializers
from .models import Pessoa, Familia, MembroFamilia, Ministerio, MembroMinisterio, PedidoOracao, Visita


class PessoaSerializer(serializers.ModelSerializer):
    idade = serializers.ReadOnlyField()
    status_membro_display = serializers.CharField(source='get_status_membro_display', read_only=True)
    estado_civil_display = serializers.CharField(source='get_estado_civil_display', read_only=True)
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    
    class Meta:
        model = Pessoa
        fields = [
            'id', 'nome_completo', 'nome_preferencia', 'cpf', 'rg', 'data_nascimento', 'idade',
            'sexo', 'estado_civil', 'estado_civil_display', 'endereco', 'cep', 'cidade', 'estado',
            'telefone', 'celular', 'email', 'profissao', 'escolaridade', 'status_membro', 
            'status_membro_display', 'data_primeira_visita', 'data_conversao', 'data_batismo', 
            'data_membresia', 'foto', 'observacoes', 'campus', 'campus_nome', 'aceite_lgpd',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class MembroFamiliaSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    parentesco_display = serializers.CharField(source='get_parentesco_display', read_only=True)
    
    class Meta:
        model = MembroFamilia
        fields = ['id', 'pessoa', 'pessoa_nome', 'parentesco', 'parentesco_display', 'responsavel_financeiro']


class FamiliaSerializer(serializers.ModelSerializer):
    membros = MembroFamiliaSerializer(many=True, read_only=True)
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    total_membros = serializers.SerializerMethodField()
    
    class Meta:
        model = Familia
        fields = [
            'id', 'nome', 'endereco', 'cep', 'cidade', 'estado', 'telefone_residencial',
            'observacoes', 'campus', 'campus_nome', 'membros', 'total_membros',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
    
    def get_total_membros(self, obj):
        return obj.membros.count()


class MembroMinisterioSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    funcao_display = serializers.CharField(source='get_funcao_display', read_only=True)
    
    class Meta:
        model = MembroMinisterio
        fields = [
            'id', 'pessoa', 'pessoa_nome', 'funcao', 'funcao_display', 
            'data_inicio', 'data_fim', 'observacoes'
        ]


class MinisterioSerializer(serializers.ModelSerializer):
    lider_nome = serializers.CharField(source='lider.nome_completo', read_only=True)
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    membros_detalhes = MembroMinisterioSerializer(source='membroministerio_set', many=True, read_only=True)
    total_membros = serializers.SerializerMethodField()
    
    class Meta:
        model = Ministerio
        fields = [
            'id', 'nome', 'descricao', 'cor', 'lider', 'lider_nome', 'campus', 'campus_nome',
            'membros_detalhes', 'total_membros', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
    
    def get_total_membros(self, obj):
        return obj.membroministerio_set.filter(data_fim__isnull=True).count()


class PedidoOracaoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    
    class Meta:
        model = PedidoOracao
        fields = [
            'id', 'titulo', 'descricao', 'publico', 'urgente', 'data_resposta', 'testemunho',
            'pessoa', 'pessoa_nome', 'responsavel', 'responsavel_nome',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class VisitaSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    visitante_nome = serializers.CharField(source='visitante.get_full_name', read_only=True)
    tipo_visita_display = serializers.CharField(source='get_tipo_visita_display', read_only=True)
    
    class Meta:
        model = Visita
        fields = [
            'id', 'data_visita', 'tipo_visita', 'tipo_visita_display', 'motivo', 'observacoes',
            'proxima_visita', 'pessoa', 'pessoa_nome', 'visitante', 'visitante_nome',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
