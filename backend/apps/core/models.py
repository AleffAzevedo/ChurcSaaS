from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Igreja(BaseModel):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    endereco = models.TextField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    site = models.URLField(blank=True)
    logo = models.ImageField(upload_to='igrejas/logos/', null=True, blank=True)
    
    plano = models.CharField(max_length=50, default='basico')
    limite_membros = models.IntegerField(default=100)
    limite_mensagens = models.IntegerField(default=1000)
    limite_storage = models.BigIntegerField(default=1073741824)  # 1GB
    
    data_vencimento = models.DateField(null=True, blank=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Igreja'
        verbose_name_plural = 'Igrejas'

    def __str__(self):
        return self.nome


class NivelOrganizacional(models.TextChoices):
    MATRIZ = 'matriz', 'Matriz'
    SETORIAL = 'setorial', 'Setorial'
    CONGREGACAO = 'congregacao', 'Congregação'


class Campus(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='campus')
    nome = models.CharField(max_length=200)
    nivel = models.CharField(max_length=20, choices=NivelOrganizacional.choices)
    campus_pai = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='filhos')
    
    endereco = models.TextField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    responsavel = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='campus_responsavel')

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campus'
        unique_together = ['igreja', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.get_nivel_display()})"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='usuarios')
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True)
    
    telefone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='usuarios/fotos/', null=True, blank=True)
    
    nivel_acesso = models.CharField(max_length=20, choices=NivelOrganizacional.choices, default=NivelOrganizacional.CONGREGACAO)
    scope_ids = models.JSONField(default=list, blank=True)
    
    ultimo_login_ip = models.GenericIPAddressField(null=True, blank=True)
    aceite_termos = models.BooleanField(default=False)
    aceite_lgpd = models.BooleanField(default=False)
    data_aceite_lgpd = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def save(self, *args, **kwargs):
        if self.aceite_lgpd and not self.data_aceite_lgpd:
            self.data_aceite_lgpd = timezone.now()
        super().save(*args, **kwargs)


class Papel(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='papeis')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    nivel_minimo = models.CharField(max_length=20, choices=NivelOrganizacional.choices)
    
    usuarios = models.ManyToManyField(User, through='UsuarioPapel', related_name='papeis')

    class Meta:
        verbose_name = 'Papel'
        verbose_name_plural = 'Papéis'
        unique_together = ['igreja', 'nome']

    def __str__(self):
        return self.nome


class Permissao(BaseModel):
    codigo = models.CharField(max_length=100, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    modulo = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'

    def __str__(self):
        return self.nome


class PapelPermissao(BaseModel):
    papel = models.ForeignKey(Papel, on_delete=models.CASCADE)
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE)
    pode_ler = models.BooleanField(default=False)
    pode_criar = models.BooleanField(default=False)
    pode_editar = models.BooleanField(default=False)
    pode_excluir = models.BooleanField(default=False)
    pode_aprovar = models.BooleanField(default=False)

    class Meta:
        unique_together = ['papel', 'permissao']

    def __str__(self):
        return f"{self.papel.nome} - {self.permissao.nome}"


class UsuarioPapel(BaseModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    papel = models.ForeignKey(Papel, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null=True, blank=True)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['usuario', 'papel', 'campus']

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.papel.nome}"


class LogAuditoria(BaseModel):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    acao = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=100)
    dados_anteriores = models.JSONField(null=True, blank=True)
    dados_novos = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.usuario} - {self.acao} - {self.modelo} - {self.created_at}"
