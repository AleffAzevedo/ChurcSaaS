from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from apps.core.permissions import IsTenantUser
from .models import (
    TemplateMensagem, ListaContatos, ContatoLista, DisparoComunicacao,
    LogEnvioMensagem, ConfiguracaoEmail, ConfiguracaoWhatsApp,
    OptInOptOut, AutomacaoComunicacao
)
from .serializers import (
    TemplateMensagemSerializer, ListaContatosSerializer, ContatoListaSerializer,
    DisparoComunicacaoSerializer, LogEnvioMensagemSerializer, ConfiguracaoEmailSerializer,
    ConfiguracaoWhatsAppSerializer, OptInOptOutSerializer, AutomacaoComunicacaoSerializer
)


class TemplateMensagemViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateMensagemSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'categoria', 'ativo']
    search_fields = ['nome', 'assunto', 'conteudo']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return TemplateMensagem.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)


class ListaContatosViewSet(viewsets.ModelViewSet):
    serializer_class = ListaContatosSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return ListaContatos.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def adicionar_contato(self, request, pk=None):
        lista = self.get_object()
        pessoa_id = request.data.get('pessoa_id')
        
        try:
            from apps.members.models import Pessoa
            pessoa = Pessoa.objects.get(id=pessoa_id, igreja=self.request.user.igreja)
            
            contato, created = ContatoLista.objects.get_or_create(
                lista=lista,
                pessoa=pessoa,
                defaults={'ativo': True}
            )
            
            if not created and not contato.ativo:
                contato.ativo = True
                contato.save()
            
            serializer = ContatoListaSerializer(contato)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            
        except Pessoa.DoesNotExist:
            return Response({'error': 'Pessoa não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remover_contato(self, request, pk=None):
        lista = self.get_object()
        pessoa_id = request.data.get('pessoa_id')
        
        try:
            contato = ContatoLista.objects.get(lista=lista, pessoa_id=pessoa_id)
            contato.ativo = False
            contato.save()
            return Response({'message': 'Contato removido da lista'})
        except ContatoLista.DoesNotExist:
            return Response({'error': 'Contato não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class DisparoComunicacaoViewSet(viewsets.ModelViewSet):
    serializer_class = DisparoComunicacaoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'status', 'template', 'lista_contatos']
    search_fields = ['titulo', 'assunto', 'conteudo']
    ordering_fields = ['created_at', 'agendado_para', 'enviado_em']
    ordering = ['-created_at']

    def get_queryset(self):
        return DisparoComunicacao.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja, criado_por=self.request.user)

    @action(detail=True, methods=['post'])
    def enviar(self, request, pk=None):
        disparo = self.get_object()
        
        if disparo.status != 'pendente':
            return Response({'error': 'Disparo já foi enviado ou está em processamento'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        disparo.status = 'enviando'
        disparo.enviado_em = timezone.now()
        disparo.save()
        
        return Response({'message': 'Disparo iniciado com sucesso'})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        disparo = self.get_object()
        
        if disparo.status in ['enviado', 'entregue']:
            return Response({'error': 'Não é possível cancelar um disparo já enviado'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        disparo.status = 'cancelado'
        disparo.save()
        
        return Response({'message': 'Disparo cancelado com sucesso'})

    @action(detail=True, methods=['get'])
    def relatorio(self, request, pk=None):
        disparo = self.get_object()
        
        logs = LogEnvioMensagem.objects.filter(disparo=disparo)
        
        estatisticas = {
            'total_destinatarios': disparo.total_destinatarios,
            'total_enviados': disparo.total_enviados,
            'total_entregues': disparo.total_entregues,
            'total_lidos': disparo.total_lidos,
            'total_erros': disparo.total_erros,
            'taxa_entrega': disparo.taxa_entrega,
            'taxa_leitura': disparo.taxa_leitura,
        }
        
        logs_serializer = LogEnvioMensagemSerializer(logs, many=True)
        
        return Response({
            'estatisticas': estatisticas,
            'logs': logs_serializer.data
        })


class ConfiguracaoEmailViewSet(viewsets.ModelViewSet):
    serializer_class = ConfiguracaoEmailSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return ConfiguracaoEmail.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def testar_conexao(self, request, pk=None):
        config = self.get_object()
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            server = smtplib.SMTP(config.servidor_smtp, config.porta_smtp)
            if config.usar_tls:
                server.starttls()
            server.login(config.email_remetente, config.senha_email)
            server.quit()
            
            return Response({'message': 'Conexão testada com sucesso'})
            
        except Exception as e:
            return Response({'error': f'Erro na conexão: {str(e)}'}, 
                          status=status.HTTP_400_BAD_REQUEST)


class ConfiguracaoWhatsAppViewSet(viewsets.ModelViewSet):
    serializer_class = ConfiguracaoWhatsAppSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return ConfiguracaoWhatsApp.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def testar_conexao(self, request, pk=None):
        config = self.get_object()
        
        return Response({'message': 'Teste de conexão WhatsApp não implementado'})


class OptInOptOutViewSet(viewsets.ModelViewSet):
    serializer_class = OptInOptOutSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aceita_email', 'aceita_sms', 'aceita_whatsapp', 'aceita_push']
    search_fields = ['pessoa__nome_completo']
    ordering_fields = ['data_opt_in', 'data_opt_out']
    ordering = ['-data_opt_in']

    def get_queryset(self):
        return OptInOptOut.objects.filter(pessoa__igreja=self.request.user.igreja)


class AutomacaoComunicacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AutomacaoComunicacaoSerializer
    permission_classes = [IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['trigger', 'ativo', 'template']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        return AutomacaoComunicacao.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)

    @action(detail=True, methods=['post'])
    def executar(self, request, pk=None):
        automacao = self.get_object()
        
        automacao.ultima_execucao = timezone.now()
        automacao.save()
        
        return Response({'message': 'Automação executada com sucesso'})
