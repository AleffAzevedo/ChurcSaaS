from django.db import models
from apps.core.models import BaseModel, Igreja, Campus, User


class TipoRelatorio(models.TextChoices):
    MEMBROS = 'membros', 'Membros'
    PRESENCA = 'presenca', 'Presença'
    FINANCEIRO = 'financeiro', 'Financeiro'
    GRUPOS = 'grupos', 'Grupos'
    EVENTOS = 'eventos', 'Eventos'
    COMUNICACAO = 'comunicacao', 'Comunicação'
    PERSONALIZADO = 'personalizado', 'Personalizado'


class RelatorioPersonalizado(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='relatorios')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TipoRelatorio.choices)
    
    query_sql = models.TextField(blank=True)
    parametros = models.JSONField(default=dict, blank=True)
    
    campos_exibicao = models.JSONField(default=list, blank=True)
    filtros_disponiveis = models.JSONField(default=list, blank=True)
    
    publico = models.BooleanField(default=False)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Relatório Personalizado'
        verbose_name_plural = 'Relatórios Personalizados'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ExecucaoRelatorio(BaseModel):
    relatorio = models.ForeignKey(RelatorioPersonalizado, on_delete=models.CASCADE, related_name='execucoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatorios_executados')
    
    parametros_utilizados = models.JSONField(default=dict, blank=True)
    data_execucao = models.DateTimeField(auto_now_add=True)
    tempo_execucao = models.FloatField(null=True, blank=True)
    
    total_registros = models.IntegerField(default=0)
    arquivo_resultado = models.FileField(upload_to='relatorios/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=[
        ('executando', 'Executando'),
        ('concluido', 'Concluído'),
        ('erro', 'Erro'),
    ], default='executando')
    
    erro_mensagem = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Execução de Relatório'
        verbose_name_plural = 'Execuções de Relatórios'
        ordering = ['-data_execucao']

    def __str__(self):
        return f"{self.relatorio.nome} - {self.data_execucao.strftime('%d/%m/%Y %H:%M')}"


class Dashboard(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='dashboards')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    
    widgets = models.JSONField(default=list, blank=True)
    layout = models.JSONField(default=dict, blank=True)
    
    publico = models.BooleanField(default=False)
    padrao = models.BooleanField(default=False)
    
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Widget(BaseModel):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets_dashboard')
    
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=[
        ('grafico_linha', 'Gráfico de Linha'),
        ('grafico_barra', 'Gráfico de Barra'),
        ('grafico_pizza', 'Gráfico de Pizza'),
        ('contador', 'Contador'),
        ('tabela', 'Tabela'),
        ('mapa', 'Mapa'),
        ('calendario', 'Calendário'),
    ])
    
    configuracao = models.JSONField(default=dict, blank=True)
    posicao_x = models.IntegerField(default=0)
    posicao_y = models.IntegerField(default=0)
    largura = models.IntegerField(default=4)
    altura = models.IntegerField(default=3)
    
    fonte_dados = models.CharField(max_length=200, blank=True)
    query_personalizada = models.TextField(blank=True)
    
    atualizar_automatico = models.BooleanField(default=True)
    intervalo_atualizacao = models.IntegerField(default=300)

    class Meta:
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'
        ordering = ['posicao_y', 'posicao_x']

    def __str__(self):
        return f"{self.dashboard.nome} - {self.nome}"
