from django.db import models
from apps.core.models import BaseModel, Igreja, Campus, User


class StatusMembro(models.TextChoices):
    VISITANTE = 'visitante', 'Visitante'
    FREQUENTADOR = 'frequentador', 'Frequentador'
    MEMBRO = 'membro', 'Membro'
    LIDER = 'lider', 'Líder'
    PASTOR = 'pastor', 'Pastor'
    INATIVO = 'inativo', 'Inativo'


class EstadoCivil(models.TextChoices):
    SOLTEIRO = 'solteiro', 'Solteiro(a)'
    CASADO = 'casado', 'Casado(a)'
    DIVORCIADO = 'divorciado', 'Divorciado(a)'
    VIUVO = 'viuvo', 'Viúvo(a)'
    UNIAO_ESTAVEL = 'uniao_estavel', 'União Estável'


class Pessoa(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='pessoas')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='pessoas')
    
    nome_completo = models.CharField(max_length=200)
    nome_preferencia = models.CharField(max_length=100, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    rg = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True)
    estado_civil = models.CharField(max_length=20, choices=EstadoCivil.choices, blank=True)
    
    endereco = models.TextField(blank=True)
    cep = models.CharField(max_length=10, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    
    telefone = models.CharField(max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    profissao = models.CharField(max_length=100, blank=True)
    escolaridade = models.CharField(max_length=50, blank=True)
    
    status_membro = models.CharField(max_length=20, choices=StatusMembro.choices, default=StatusMembro.VISITANTE)
    data_primeira_visita = models.DateField(null=True, blank=True)
    data_conversao = models.DateField(null=True, blank=True)
    data_batismo = models.DateField(null=True, blank=True)
    data_membresia = models.DateField(null=True, blank=True)
    
    foto = models.ImageField(upload_to='pessoas/fotos/', null=True, blank=True)
    observacoes = models.TextField(blank=True)
    
    aceite_lgpd = models.BooleanField(default=False)
    data_aceite_lgpd = models.DateTimeField(null=True, blank=True)
    
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pessoa')

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        unique_together = ['igreja', 'cpf']
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

    @property
    def idade(self):
        if self.data_nascimento:
            from datetime import date
            today = date.today()
            return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return None


class Familia(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='familias')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='familias')
    
    nome = models.CharField(max_length=200)
    endereco = models.TextField(blank=True)
    cep = models.CharField(max_length=10, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    
    telefone_residencial = models.CharField(max_length=20, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Família'
        verbose_name_plural = 'Famílias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class TipoParentesco(models.TextChoices):
    CHEFE = 'chefe', 'Chefe da Família'
    CONJUGE = 'conjuge', 'Cônjuge'
    FILHO = 'filho', 'Filho(a)'
    PAI = 'pai', 'Pai/Mãe'
    IRMAO = 'irmao', 'Irmão/Irmã'
    OUTRO = 'outro', 'Outro'


class MembroFamilia(BaseModel):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='membros')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='familias')
    parentesco = models.CharField(max_length=20, choices=TipoParentesco.choices)
    responsavel_financeiro = models.BooleanField(default=False)

    class Meta:
        unique_together = ['familia', 'pessoa']
        verbose_name = 'Membro da Família'
        verbose_name_plural = 'Membros da Família'

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.familia.nome}"


class Ministerio(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='ministerios')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='ministerios', null=True, blank=True)
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    cor = models.CharField(max_length=7, default='#007bff')
    
    lider = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='ministerios_liderados')
    membros = models.ManyToManyField(Pessoa, through='MembroMinisterio', related_name='ministerios')

    class Meta:
        verbose_name = 'Ministério'
        verbose_name_plural = 'Ministérios'
        unique_together = ['igreja', 'nome']
        ordering = ['nome']

    def __str__(self):
        return self.nome


class TipoFuncao(models.TextChoices):
    LIDER = 'lider', 'Líder'
    VICE_LIDER = 'vice_lider', 'Vice-Líder'
    SECRETARIO = 'secretario', 'Secretário'
    TESOUREIRO = 'tesoureiro', 'Tesoureiro'
    MEMBRO = 'membro', 'Membro'


class MembroMinisterio(BaseModel):
    ministerio = models.ForeignKey(Ministerio, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    funcao = models.CharField(max_length=20, choices=TipoFuncao.choices, default=TipoFuncao.MEMBRO)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ['ministerio', 'pessoa']
        verbose_name = 'Membro do Ministério'
        verbose_name_plural = 'Membros do Ministério'

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.ministerio.nome}"


class PedidoOracao(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='pedidos_oracao')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='pedidos_oracao')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    publico = models.BooleanField(default=False)
    urgente = models.BooleanField(default=False)
    
    data_resposta = models.DateField(null=True, blank=True)
    testemunho = models.TextField(blank=True)
    
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Pedido de Oração'
        verbose_name_plural = 'Pedidos de Oração'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo} - {self.pessoa.nome_completo}"


class Visita(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='visitas')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='visitas')
    visitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitas_realizadas')
    
    data_visita = models.DateTimeField()
    tipo_visita = models.CharField(max_length=50, choices=[
        ('pastoral', 'Pastoral'),
        ('evangelistica', 'Evangelística'),
        ('social', 'Social'),
        ('acompanhamento', 'Acompanhamento'),
    ])
    
    motivo = models.TextField()
    observacoes = models.TextField(blank=True)
    proxima_visita = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-data_visita']

    def __str__(self):
        return f"Visita a {self.pessoa.nome_completo} - {self.data_visita.strftime('%d/%m/%Y')}"
