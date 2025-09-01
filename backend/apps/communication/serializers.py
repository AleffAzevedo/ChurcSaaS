from rest_framework import serializers
from .models import (
    TemplateMensagem, ListaContatos, ContatoLista, DisparoComunicacao,
    LogEnvioMensagem, ConfiguracaoEmail, ConfiguracaoWhatsApp,
    OptInOptOut, AutomacaoComunicacao
)


class TemplateMensagemSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    
    class Meta:
        model = TemplateMensagem
        fields = [
            'id', 'nome', 'tipo', 'tipo_display', 'assunto', 'conteudo',
            'variaveis_disponiveis', 'categoria', 'categoria_display', 'ativo',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class ContatoListaSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    pessoa_email = serializers.CharField(source='pessoa.email', read_only=True)
    pessoa_telefone = serializers.CharField(source='pessoa.celular', read_only=True)
    
    class Meta:
        model = ContatoLista
        fields = ['id', 'pessoa', 'pessoa_nome', 'pessoa_email', 'pessoa_telefone', 'data_adicao', 'ativo']


class ListaContatosSerializer(serializers.ModelSerializer):
    contatos_detalhes = ContatoListaSerializer(source='contatolista_set', many=True, read_only=True)
    total_contatos = serializers.ReadOnlyField()
    
    class Meta:
        model = ListaContatos
        fields = [
            'id', 'nome', 'descricao', 'filtros', 'contatos_detalhes', 'total_contatos',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class DisparoComunicacaoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    template_nome = serializers.CharField(source='template.nome', read_only=True)
    lista_contatos_nome = serializers.CharField(source='lista_contatos.nome', read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    taxa_entrega = serializers.ReadOnlyField()
    taxa_leitura = serializers.ReadOnlyField()
    
    class Meta:
        model = DisparoComunicacao
        fields = [
            'id', 'titulo', 'tipo', 'tipo_display', 'template', 'template_nome',
            'assunto', 'conteudo', 'lista_contatos', 'lista_contatos_nome',
            'agendado_para', 'enviado_em', 'total_destinatarios', 'total_enviados',
            'total_entregues', 'total_lidos', 'total_erros', 'criado_por', 'criado_por_nome',
            'status', 'status_display', 'taxa_entrega', 'taxa_leitura',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']


class LogEnvioMensagemSerializer(serializers.ModelSerializer):
    disparo_titulo = serializers.CharField(source='disparo.titulo', read_only=True)
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = LogEnvioMensagem
        fields = [
            'id', 'disparo', 'disparo_titulo', 'pessoa', 'pessoa_nome', 'destinatario',
            'status', 'status_display', 'data_envio', 'data_entrega', 'data_leitura',
            'erro_mensagem', 'tentativas', 'id_externo', 'webhook_data',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConfiguracaoEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoEmail
        fields = [
            'id', 'servidor_smtp', 'porta_smtp', 'usar_tls', 'email_remetente',
            'nome_remetente', 'senha_email', 'ativo', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
        extra_kwargs = {
            'senha_email': {'write_only': True}
        }


class ConfiguracaoWhatsAppSerializer(serializers.ModelSerializer):
    provedor_display = serializers.CharField(source='get_provedor_display', read_only=True)
    
    class Meta:
        model = ConfiguracaoWhatsApp
        fields = [
            'id', 'api_token', 'numero_telefone', 'webhook_url', 'provedor', 'provedor_display',
            'configuracoes_extras', 'ativo', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_token': {'write_only': True}
        }


class OptInOptOutSerializer(serializers.ModelSerializer):
    pessoa_nome = serializers.CharField(source='pessoa.nome_completo', read_only=True)
    
    class Meta:
        model = OptInOptOut
        fields = [
            'id', 'pessoa', 'pessoa_nome', 'aceita_email', 'aceita_sms', 'aceita_whatsapp',
            'aceita_push', 'data_opt_in', 'data_opt_out', 'motivo_opt_out',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AutomacaoComunicacaoSerializer(serializers.ModelSerializer):
    trigger_display = serializers.CharField(source='get_trigger_display', read_only=True)
    template_nome = serializers.CharField(source='template.nome', read_only=True)
    
    class Meta:
        model = AutomacaoComunicacao
        fields = [
            'id', 'nome', 'descricao', 'trigger', 'trigger_display', 'condicoes',
            'template', 'template_nome', 'delay_dias', 'ativo', 'ultima_execucao',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'igreja', 'created_at', 'updated_at']
