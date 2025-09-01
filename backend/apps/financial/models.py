from django.db import models
from apps.core.models import BaseModel, Igreja, Campus, User
from apps.members.models import Pessoa


class TipoLancamento(models.TextChoices):
    ENTRADA = 'entrada', 'Entrada'
    SAIDA = 'saida', 'Saída'


class TipoEntrada(models.TextChoices):
    DIZIMO = 'dizimo', 'Dízimo'
    OFERTA = 'oferta', 'Oferta'
    CAMPANHA = 'campanha', 'Campanha'
    DOACAO = 'doacao', 'Doação'
    EVENTO = 'evento', 'Evento'
    OUTROS = 'outros', 'Outros'


class FormaPagamento(models.TextChoices):
    DINHEIRO = 'dinheiro', 'Dinheiro'
    PIX = 'pix', 'PIX'
    CARTAO_DEBITO = 'cartao_debito', 'Cartão de Débito'
    CARTAO_CREDITO = 'cartao_credito', 'Cartão de Crédito'
    BOLETO = 'boleto', 'Boleto'
    TRANSFERENCIA = 'transferencia', 'Transferência'
    CHEQUE = 'cheque', 'Cheque'


class Categoria(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=10, choices=TipoLancamento.choices)
    cor = models.CharField(max_length=7, default='#007bff')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ['igreja', 'nome']
        ordering = ['nome']

    def __str__(self):
        return self.nome


class CentroCusto(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='centros_custo')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='centros_custo', null=True, blank=True)
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    codigo = models.CharField(max_length=20, blank=True)
    
    responsavel = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'
        unique_together = ['igreja', 'nome']
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ContaBancaria(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='contas_bancarias')
    
    nome = models.CharField(max_length=100)
    banco = models.CharField(max_length=100)
    agencia = models.CharField(max_length=20)
    conta = models.CharField(max_length=20)
    tipo_conta = models.CharField(max_length=20, choices=[
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Poupança'),
        ('aplicacao', 'Aplicação'),
    ])
    
    saldo_inicial = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.banco}"

    @property
    def saldo_atual(self):
        entradas = self.lancamentos.filter(tipo='entrada').aggregate(
            total=models.Sum('valor')
        )['total'] or 0
        
        saidas = self.lancamentos.filter(tipo='saida').aggregate(
            total=models.Sum('valor')
        )['total'] or 0
        
        return self.saldo_inicial + entradas - saidas


class LancamentoFinanceiro(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='lancamentos')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='lancamentos', null=True, blank=True)
    
    tipo = models.CharField(max_length=10, choices=TipoLancamento.choices)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='lancamentos')
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.SET_NULL, null=True, blank=True, related_name='lancamentos')
    conta_bancaria = models.ForeignKey(ContaBancaria, on_delete=models.CASCADE, related_name='lancamentos')
    
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    data_lancamento = models.DateField()
    data_vencimento = models.DateField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    
    forma_pagamento = models.CharField(max_length=20, choices=FormaPagamento.choices, blank=True)
    numero_documento = models.CharField(max_length=50, blank=True)
    
    pessoa = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='lancamentos')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lancamentos_responsavel')
    
    observacoes = models.TextField(blank=True)
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    
    aprovado = models.BooleanField(default=False)
    aprovado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lancamentos_aprovados')
    data_aprovacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Lançamento Financeiro'
        verbose_name_plural = 'Lançamentos Financeiros'
        ordering = ['-data_lancamento']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} - R$ {self.valor}"

    @property
    def status_pagamento(self):
        if self.data_pagamento:
            return 'Pago'
        elif self.data_vencimento and self.data_vencimento < timezone.now().date():
            return 'Vencido'
        else:
            return 'Pendente'


class Campanha(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='campanhas')
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    meta_valor = models.DecimalField(max_digits=15, decimal_places=2)
    
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    responsavel = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, related_name='campanhas_responsavel')
    
    imagem = models.ImageField(upload_to='campanhas/', null=True, blank=True)
    cor = models.CharField(max_length=7, default='#28a745')

    class Meta:
        verbose_name = 'Campanha'
        verbose_name_plural = 'Campanhas'
        ordering = ['-data_inicio']

    def __str__(self):
        return self.nome

    @property
    def valor_arrecadado(self):
        return self.lancamentos.filter(
            tipo='entrada',
            aprovado=True
        ).aggregate(total=models.Sum('valor'))['total'] or 0

    @property
    def percentual_meta(self):
        if self.meta_valor > 0:
            return (self.valor_arrecadado / self.meta_valor) * 100
        return 0


class LancamentoCampanha(BaseModel):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='lancamentos')
    lancamento = models.ForeignKey(LancamentoFinanceiro, on_delete=models.CASCADE, related_name='campanhas')

    class Meta:
        unique_together = ['campanha', 'lancamento']

    def __str__(self):
        return f"{self.campanha.nome} - {self.lancamento.descricao}"


class Orcamento(BaseModel):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE, related_name='orcamentos')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='orcamentos', null=True, blank=True)
    
    nome = models.CharField(max_length=200)
    ano = models.IntegerField()
    mes = models.IntegerField(null=True, blank=True)
    
    valor_previsto_entrada = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_previsto_saida = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    aprovado = models.BooleanField(default=False)
    aprovado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        unique_together = ['igreja', 'ano', 'mes']
        ordering = ['-ano', '-mes']

    def __str__(self):
        if self.mes:
            return f"{self.nome} - {self.mes:02d}/{self.ano}"
        return f"{self.nome} - {self.ano}"


class ItemOrcamento(BaseModel):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='itens')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.SET_NULL, null=True, blank=True)
    
    descricao = models.CharField(max_length=200)
    valor_previsto = models.DecimalField(max_digits=15, decimal_places=2)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Item do Orçamento'
        verbose_name_plural = 'Itens do Orçamento'

    def __str__(self):
        return f"{self.orcamento.nome} - {self.descricao}"

    @property
    def valor_realizado(self):
        return LancamentoFinanceiro.objects.filter(
            categoria=self.categoria,
            centro_custo=self.centro_custo,
            data_lancamento__year=self.orcamento.ano,
            data_lancamento__month=self.orcamento.mes or 1,
            aprovado=True
        ).aggregate(total=models.Sum('valor'))['total'] or 0
