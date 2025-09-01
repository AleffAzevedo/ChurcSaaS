from rest_framework import serializers
from .models import RelatorioPersonalizado, ExecucaoRelatorio, Dashboard, Widget


class RelatorioPersonalizadoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    
    class Meta:
        model = RelatorioPersonalizado
        fields = [
            'id', 'nome', 'descricao', 'tipo', 'tipo_display', 'query_sql', 'parametros',
            'campos_exibicao', 'filtros_disponiveis', 'publico', 'criado_por', 'criado_por_nome',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class ExecucaoRelatorioSerializer(serializers.ModelSerializer):
    relatorio_nome = serializers.CharField(source='relatorio.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ExecucaoRelatorio
        fields = [
            'id', 'relatorio', 'relatorio_nome', 'usuario', 'usuario_nome',
            'parametros_utilizados', 'data_execucao', 'tempo_execucao',
            'total_registros', 'arquivo_resultado', 'status', 'status_display',
            'erro_mensagem', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'data_execucao', 'created_at', 'updated_at']


class WidgetSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Widget
        fields = [
            'id', 'nome', 'tipo', 'tipo_display', 'configuracao', 'posicao_x', 'posicao_y',
            'largura', 'altura', 'fonte_dados', 'query_personalizada',
            'atualizar_automatico', 'intervalo_atualizacao'
        ]


class DashboardSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    widgets_dashboard = WidgetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dashboard
        fields = [
            'id', 'nome', 'descricao', 'widgets', 'layout', 'publico', 'padrao',
            'criado_por', 'criado_por_nome', 'widgets_dashboard',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
