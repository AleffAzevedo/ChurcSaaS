from django.db import models
from apps.core.models import BaseModel, Igreja, Campus
from apps.members.models import Pessoa, Ministerio


class TipoEvento(models.TextChoices):
    CULTO = 'culto', 'Culto'
    REUNIAO = 'reuniao', 'Reunião'
    CURSO = 'curso', 'Curso'
    CONFERENCIA = 'conferencia', 'Conferência'
    RETIRO = 'retiro', 'Retiro'
    EVANGELISMO = 'evangelismo', 'Evangelismo'
    SOCIAL = 'social', 'Social'
    CASAMENTO = 'casamento', 'Casamento'
    FUNERAL = 'funeral', 'Funeral'
    BATISMO = 'batismo', 'Batismo'
    CEIA = 'ceia', 'Santa Ceia'


class Evento(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='eventos')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='eventos')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TipoEvento.choices, default=TipoEvento.CULTO)
    
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    
    local = models.CharField(max_length=200, blank=True)
    endereco = models.TextField(blank=True)
    
    publico = models.BooleanField(default=True)
    requer_inscricao = models.BooleanField(default=False)
    limite_inscricoes = models.IntegerField(null=True, blank=True)
    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    responsavel = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos_responsaveis')
    ministerio = models.ForeignKey(Ministerio, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos')
    
    cor = models.CharField(max_length=7, default='#007bff')
    imagem = models.ImageField(upload_to='eventos/imagens/', null=True, blank=True)
    
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data_inicio']

    def __str__(self):
        return f"{self.titulo} - {self.data_inicio.strftime('%d/%m/%Y %H:%M')}"

    @property
    def total_inscricoes(self):
        return self.inscricoes.filter(status='confirmada').count()

    @property
    def vagas_disponiveis(self):
        if self.limite_inscricoes:
            return self.limite_inscricoes - self.total_inscricoes
        return None


class StatusInscricao(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    CONFIRMADA = 'confirmada', 'Confirmada'
    CANCELADA = 'cancelada', 'Cancelada'
    PRESENTE = 'presente', 'Presente'


class InscricaoEvento(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='inscricoes_eventos')
    
    status = models.CharField(max_length=20, choices=StatusInscricao.choices, default=StatusInscricao.PENDENTE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    data_confirmacao = models.DateTimeField(null=True, blank=True)
    
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pagamento = models.CharField(max_length=50, blank=True)
    
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['evento', 'pessoa']
        verbose_name = 'Inscrição no Evento'
        verbose_name_plural = 'Inscrições no Evento'

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.evento.titulo}"


class TipoEscala(models.TextChoices):
    LOUVOR = 'louvor', 'Louvor'
    MULTIMIDIA = 'multimidia', 'Multimídia'
    RECEPCAO = 'recepcao', 'Recepção'
    KIDS = 'kids', 'Kids'
    SEGURANCA = 'seguranca', 'Segurança'
    LIMPEZA = 'limpeza', 'Limpeza'
    ESTACIONAMENTO = 'estacionamento', 'Estacionamento'
    DIACONIA = 'diaconia', 'Diaconia'


class EscalaEvento(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='escalas')
    tipo = models.CharField(max_length=20, choices=TipoEscala.choices)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='escalas_eventos')
    
    funcao = models.CharField(max_length=100, blank=True)
    horario_inicio = models.TimeField(null=True, blank=True)
    horario_fim = models.TimeField(null=True, blank=True)
    
    confirmado = models.BooleanField(default=False)
    data_confirmacao = models.DateTimeField(null=True, blank=True)
    
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['evento', 'tipo', 'pessoa']
        verbose_name = 'Escala do Evento'
        verbose_name_plural = 'Escalas do Evento'

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.get_tipo_display()} - {self.evento.titulo}"


class PresencaEvento(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='presencas')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='presencas_eventos')
    
    presente = models.BooleanField(default=True)
    horario_chegada = models.DateTimeField(null=True, blank=True)
    horario_saida = models.DateTimeField(null=True, blank=True)
    
    visitante = models.BooleanField(default=False)
    primeira_visita = models.BooleanField(default=False)
    
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['evento', 'pessoa']
        verbose_name = 'Presença no Evento'
        verbose_name_plural = 'Presenças no Evento'

    def __str__(self):
        status = "Presente" if self.presente else "Ausente"
        return f"{self.pessoa.nome_completo} - {status}"


class CheckInEvento(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='checkins')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='checkins_eventos')
    
    codigo_qr = models.CharField(max_length=100, unique=True)
    data_checkin = models.DateTimeField(auto_now_add=True)
    
    responsavel_checkin = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='checkins_realizados')
    
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['evento', 'pessoa']
        verbose_name = 'Check-in do Evento'
        verbose_name_plural = 'Check-ins do Evento'

    def __str__(self):
        return f"Check-in: {self.pessoa.nome_completo} - {self.evento.titulo}"


class RecursoEvento(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='recursos')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='recursos', null=True, blank=True)
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=[
        ('sala', 'Sala'),
        ('equipamento', 'Equipamento'),
        ('veiculo', 'Veículo'),
        ('material', 'Material'),
    ])
    
    capacidade = models.IntegerField(null=True, blank=True)
    localizacao = models.CharField(max_length=200, blank=True)
    
    disponivel = models.BooleanField(default=True)
    requer_aprovacao = models.BooleanField(default=False)
    
    responsavel = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ReservaRecurso(BaseModel):
    recurso = models.ForeignKey(RecursoEvento, on_delete=models.CASCADE, related_name='reservas')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='recursos_reservados')
    
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    
    solicitante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='reservas_solicitadas')
    aprovado_por = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas_aprovadas')
    
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
        ('cancelada', 'Cancelada'),
    ], default='pendente')
    
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Reserva de Recurso'
        verbose_name_plural = 'Reservas de Recursos'

    def __str__(self):
        return f"{self.recurso.nome} - {self.evento.titulo}"
