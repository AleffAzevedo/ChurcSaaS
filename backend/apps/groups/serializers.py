from rest_framework import serializers
from .models import Grupo, MembroGrupo, Reuniao, PresencaReuniao, MaterialEstudo, GrupoMaterial


class MembroGrupoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MembroGrupo
        fields = [
            'id', 'pessoa', 'pessoa_nome', 'status', 'status_display',
            'data_entrada', 'data_saida', 'observacoes'
        ]


class GrupoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    dia_reuniao_display = serializers.CharField(source='get_dia_reuniao_display', read_only=True)
    lider_nome = serializers.CharField(source='lider.nome_completo', read_only=True)
    vice_lider_nome = serializers.CharField(source='vice_lider.nome_completo', read_only=True)
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    membros_detalhes = MembroGrupoSerializer(source='membrogrupo_set', many=True, read_only=True)
    total_membros = serializers.ReadOnlyField()
    percentual_meta = serializers.ReadOnlyField()
    
    class Meta:
        model = Grupo
        fields = [
            'id', 'nome', 'descricao', 'tipo', 'tipo_display', 'lider', 'lider_nome',
            'vice_lider', 'vice_lider_nome', 'endereco', 'dia_reuniao', 'dia_reuniao_display',
            'horario_reuniao', 'meta_membros', 'meta_multiplicacao', 'cor', 'foto',
            'campus', 'campus_nome', 'membros_detalhes', 'total_membros', 'percentual_meta',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class PresencaReuniaoSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    
    class Meta:
        model = PresencaReuniao
        fields = ['id', 'pessoa', 'pessoa_nome', 'presente', 'visitante', 'observacoes']


class ReuniaoSerializer(serializers.ModelSerializer):
    grupo_nome = serializers.CharField(source='grupo.nome', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.nome_completo', read_only=True)
    presencas = PresencaReuniaoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reuniao
        fields = [
            'id', 'data_reuniao', 'tema', 'versiculo', 'resumo', 'total_presentes',
            'total_visitantes', 'total_conversoes', 'oferta', 'responsavel', 'responsavel_nome',
            'observacoes', 'grupo', 'grupo_nome', 'presencas',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MaterialEstudoSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    
    class Meta:
        model = MaterialEstudo
        fields = [
            'id', 'titulo', 'descricao', 'conteudo', 'categoria', 'categoria_display',
            'arquivo', 'link_externo', 'autor', 'data_publicacao',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class GrupoMaterialSerializer(serializers.ModelSerializer):
    grupo_nome = serializers.CharField(source='grupo.nome', read_only=True)
    material_titulo = serializers.CharField(source='material.titulo', read_only=True)
    
    class Meta:
        model = GrupoMaterial
        fields = [
            'id', 'grupo', 'grupo_nome', 'material', 'material_titulo',
            'data_inicio', 'data_fim', 'observacoes'
        ]
