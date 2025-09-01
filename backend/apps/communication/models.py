from django.db import models
from apps.core.models import BaseModel, Igreja, Campus, User
from apps.members.models import Pessoa, Ministerio


class TipoMensagem(models.TextChoices):
    EMAIL = 'email', 'E-mail'
    SMS = 'sms', 'SMS'
    WHATSAPP = 'whatsapp', 'WhatsApp'
    PUSH = 'push', 'Push Notification'


class StatusEnvio(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    ENVIANDO = 'enviando', 'Enviando'
    ENVIADO = 'enviado', 'Enviado'
    ENTREGUE = 'entregue', 'Entregue'
    LIDO = 'lido', 'Lido'
    ERRO = 'erro', 'Erro'
    CANCELADO = 'cancelado', 'Cancelado'


class TemplateMensagem(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='templates_mensagem')
    
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TipoMensagem.choices)
    assunto = models.CharField(max_length=200, blank=True)
    conteudo = models.TextField()
    
    variaveis_disponiveis = models.JSONField(default=list, blank=True)
    
    categoria = models.CharField(max_length=50, choices=[
        ('boas_vindas', 'Boas-vindas'),
        ('aniversario', 'Aniversário'),
        ('evento', 'Evento'),
        ('lembrete', 'Lembrete'),
        ('pastoral', 'Pastoral'),
        ('financeiro', 'Financeiro'),
        ('geral', 'Geral'),
    ])
    
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Template de Mensagem'
        verbose_name_plural = 'Templates de Mensagem'
        unique_together = ['igreja', 'nome']
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class ListaContatos(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='listas_contatos')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    
    filtros = models.JSONField(default=dict, blank=True)
    
    contatos = models.ManyToManyField(Pessoa, through='ContatoLista', related_name='listas_contatos')

    class Meta:
        verbose_name = 'Lista de Contatos'
        verbose_name_plural = 'Listas de Contatos'
        unique_together = ['igreja', 'nome']
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def total_contatos(self):
        return self.contatos.count()


class ContatoLista(BaseModel):
    lista = models.ForeignKey(ListaContatos, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = ['lista', 'pessoa']

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.lista.nome}"


class DisparoComunicacao(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='disparos')
    
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TipoMensagem.choices)
    template = models.ForeignKey(TemplateMensagem, on_delete=models.SET_NULL, null=True, blank=True)
    
    assunto = models.CharField(max_length=200, blank=True)
    conteudo = models.TextField()
    
    lista_contatos = models.ForeignKey(ListaContatos, on_delete=models.SET_NULL, null=True, blank=True)
    contatos_individuais = models.ManyToManyField(Pessoa, blank=True, related_name='disparos_recebidos')
    
    agendado_para = models.DateTimeField(null=True, blank=True)
    enviado_em = models.DateTimeField(null=True, blank=True)
    
    total_destinatarios = models.IntegerField(default=0)
    total_enviados = models.IntegerField(default=0)
    total_entregues = models.IntegerField(default=0)
    total_lidos = models.IntegerField(default=0)
    total_erros = models.IntegerField(default=0)
    
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=StatusEnvio.choices, default=StatusEnvio.PENDENTE)

    class Meta:
        verbose_name = 'Disparo de Comunicação'
        verbose_name_plural = 'Disparos de Comunicação'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"

    @property
    def taxa_entrega(self):
        if self.total_enviados > 0:
            return (self.total_entregues / self.total_enviados) * 100
        return 0

    @property
    def taxa_leitura(self):
        if self.total_entregues > 0:
            return (self.total_lidos / self.total_entregues) * 100
        return 0


class LogEnvioMensagem(BaseModel):
    disparo = models.ForeignKey(DisparoComunicacao, on_delete=models.CASCADE, related_name='logs_envio')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='logs_mensagens')
    
    destinatario = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=StatusEnvio.choices, default=StatusEnvio.PENDENTE)
    
    data_envio = models.DateTimeField(null=True, blank=True)
    data_entrega = models.DateTimeField(null=True, blank=True)
    data_leitura = models.DateTimeField(null=True, blank=True)
    
    erro_mensagem = models.TextField(blank=True)
    tentativas = models.IntegerField(default=0)
    
    id_externo = models.CharField(max_length=200, blank=True)
    webhook_data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Log de Envio'
        verbose_name_plural = 'Logs de Envio'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.get_status_display()}"


class ConfiguracaoEmail(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='config_email')
    
    servidor_smtp = models.CharField(max_length=200, default='smtp.gmail.com')
    porta_smtp = models.IntegerField(default=587)
    usar_tls = models.BooleanField(default=True)
    
    email_remetente = models.EmailField()
    nome_remetente = models.CharField(max_length=200)
    senha_email = models.CharField(max_length=200)
    
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Configuração de E-mail'
        verbose_name_plural = 'Configurações de E-mail'

    def __str__(self):
        return f"{self.nome_remetente} <{self.email_remetente}>"


class ConfiguracaoWhatsApp(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='config_whatsapp')
    
    api_token = models.CharField(max_length=500)
    numero_telefone = models.CharField(max_length=20)
    webhook_url = models.URLField(blank=True)
    
    provedor = models.CharField(max_length=50, choices=[
        ('whatsapp_business', 'WhatsApp Business API'),
        ('twilio', 'Twilio'),
        ('chatapi', 'ChatAPI'),
        ('evolution', 'Evolution API'),
    ])
    
    configuracoes_extras = models.JSONField(default=dict, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Configuração do WhatsApp'
        verbose_name_plural = 'Configurações do WhatsApp'

    def __str__(self):
        return f"{self.get_provedor_display()} - {self.numero_telefone}"


class OptInOptOut(BaseModel):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='preferencias_comunicacao')
    
    aceita_email = models.BooleanField(default=True)
    aceita_sms = models.BooleanField(default=True)
    aceita_whatsapp = models.BooleanField(default=True)
    aceita_push = models.BooleanField(default=True)
    
    data_opt_in = models.DateTimeField(auto_now_add=True)
    data_opt_out = models.DateTimeField(null=True, blank=True)
    
    motivo_opt_out = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Preferência de Comunicação'
        verbose_name_plural = 'Preferências de Comunicação'

    def __str__(self):
        return f"{self.pessoa.nome_completo} - Preferências"


class AutomacaoComunicacao(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='automacoes')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    
    trigger = models.CharField(max_length=50, choices=[
        ('novo_membro', 'Novo Membro'),
        ('aniversario', 'Aniversário'),
        ('ausencia_culto', 'Ausência no Culto'),
        ('data_especifica', 'Data Específica'),
        ('evento_personalizado', 'Evento Personalizado'),
    ])
    
    condicoes = models.JSONField(default=dict, blank=True)
    template = models.ForeignKey(TemplateMensagem, on_delete=models.CASCADE)
    
    delay_dias = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    
    ultima_execucao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Automação de Comunicação'
        verbose_name_plural = 'Automações de Comunicação'
        ordering = ['nome']

    def __str__(self):
        return self.nome
