from django.db import models
from apps.core.models import BaseModel, Igreja, Campus
from apps.members.models import Pessoa


class TipoGrupo(models.TextChoices):
    CELULA = 'celula', 'Célula'
    GRUPO_PEQUENO = 'grupo_pequeno', 'Grupo Pequeno'
    CLASSE = 'classe', 'Classe'
    MINISTERIO = 'ministerio', 'Ministério'
    DEPARTAMENTO = 'departamento', 'Departamento'


class Grupo(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='grupos')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='grupos')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TipoGrupo.choices, default=TipoGrupo.CELULA)
    
    lider = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos_liderados')
    vice_lider = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos_vice_liderados')
    
    endereco = models.TextField(blank=True)
    dia_reuniao = models.CharField(max_length=20, choices=[
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ], blank=True)
    horario_reuniao = models.TimeField(null=True, blank=True)
    
    meta_membros = models.IntegerField(default=12)
    meta_multiplicacao = models.DateField(null=True, blank=True)
    
    cor = models.CharField(max_length=7, default='#007bff')
    foto = models.ImageField(upload_to='grupos/fotos/', null=True, blank=True)
    
    membros = models.ManyToManyField(Pessoa, through='MembroGrupo', related_name='grupos')

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        unique_together = ['igreja', 'nome']
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def total_membros(self):
        return self.membrogrupo_set.filter(data_saida__isnull=True).count()

    @property
    def percentual_meta(self):
        if self.meta_membros > 0:
            return (self.total_membros / self.meta_membros) * 100
        return 0


class StatusMembroGrupo(models.TextChoices):
    ATIVO = 'ativo', 'Ativo'
    INATIVO = 'inativo', 'Inativo'
    LIDER = 'lider', 'Líder'
    VICE_LIDER = 'vice_lider', 'Vice-Líder'
    SECRETARIO = 'secretario', 'Secretário'


class MembroGrupo(BaseModel):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusMembroGrupo.choices, default=StatusMembroGrupo.ATIVO)
    data_entrada = models.DateField()
    data_saida = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['grupo', 'pessoa']
        verbose_name = 'Membro do Grupo'
        verbose_name_plural = 'Membros do Grupo'

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.grupo.nome}"


class Reuniao(BaseModel):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='reunioes')
    
    data_reuniao = models.DateTimeField()
    tema = models.CharField(max_length=200)
    versiculo = models.CharField(max_length=500, blank=True)
    resumo = models.TextField(blank=True)
    
    total_presentes = models.IntegerField(default=0)
    total_visitantes = models.IntegerField(default=0)
    total_conversoes = models.IntegerField(default=0)
    
    oferta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    responsavel = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Reunião'
        verbose_name_plural = 'Reuniões'
        ordering = ['-data_reuniao']

    def __str__(self):
        return f"{self.grupo.nome} - {self.data_reuniao.strftime('%d/%m/%Y')}"


class PresencaReuniao(BaseModel):
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, related_name='presencas')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='presencas_reuniao')
    
    presente = models.BooleanField(default=True)
    visitante = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['reuniao', 'pessoa']
        verbose_name = 'Presença na Reunião'
        verbose_name_plural = 'Presenças na Reunião'

    def __str__(self):
        status = "Presente" if self.presente else "Ausente"
        return f"{self.pessoa.nome_completo} - {status}"


class MaterialEstudo(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='materiais_estudo')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    conteudo = models.TextField()
    
    categoria = models.CharField(max_length=50, choices=[
        ('celula', 'Célula'),
        ('discipulado', 'Discipulado'),
        ('lideranca', 'Liderança'),
        ('evangelismo', 'Evangelismo'),
        ('familia', 'Família'),
        ('jovens', 'Jovens'),
        ('criancas', 'Crianças'),
    ])
    
    arquivo = models.FileField(upload_to='materiais/', null=True, blank=True)
    link_externo = models.URLField(blank=True)
    
    autor = models.CharField(max_length=100, blank=True)
    data_publicacao = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Material de Estudo'
        verbose_name_plural = 'Materiais de Estudo'
        ordering = ['-data_publicacao', 'titulo']

    def __str__(self):
        return self.titulo


class GrupoMaterial(BaseModel):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialEstudo, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['grupo', 'material']
        verbose_name = 'Material do Grupo'
        verbose_name_plural = 'Materiais do Grupo'

    def __str__(self):
        return f"{self.grupo.nome} - {self.material.titulo}"
