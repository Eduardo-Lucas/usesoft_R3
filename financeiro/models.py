# coding=utf-8
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models


# Validators
from choices.models import SIM_NAO_CHOICES, TIPO_DOCUMENTO_CHOICES, INDICADOR_PAGAMENTO_CHOICES


def validate_maior_que_zero(value):
    if value <= 0:
        raise ValidationError(
            'O código da Conta tem que ser MAIOR QUE ZERO',
            params={'value': value},
        )


def validate_valor_minimo(value):
    if value <= 0:
        raise ValidationError(
            'O valor do lançamento NÃO PODE SER ZERO ou MENOR QUE ZERO. O valor mínimo permitido é: R$ 0,01',
            params={'value': value},
        )


valor_numerico = RegexValidator(r'^[0-9]*$', 'Apenas valores numéricos, de 0 até 9, são permitidos.')


# ---------------------------------------------------------------------------------------------------------------------
# ARQUIVO CODIGOS DE BANCOS - TABELAS GENERICAS DO SISTEMA USESOFTR3
# (usesoft=KCCI05)
# D:\projeto\USESOFTR3\tabelasglobais\Codigos_bancos.txt
# ---------------------------------------------------------------------------------------------------------------------
class CodigosBancos(models.Model):
    codigo = models.CharField(null=False, unique=True, max_length=5)
    agencia = models.CharField(null=False, unique=True, max_length=7)
    descricao = models.CharField(max_length=60, null=False)
    email = models.CharField(max_length=50, null=False)

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite  este banco caso sua empresa não o utilize ou utilize muito '
                                            'esporadicamente  para evitar erros')

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ('descricao',)


# ----------------------------------------------------------------------------------------------------------------------
# ARQUIVO DE NATUREZAS DE CUSTOS financeiras DA EMPRESA - TABELAS GENERICAS DO SISTEMA USESOFTR3
# (usesoft=KCCI55)
# ----------------------------------------------------------------------------------------------------------------------
class NaturezaCusto(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(999999)],
                                         help_text='Codigo da natureza financeira do centro de custos - '
                                                   'verbas destinadas aos centros de custos')
    descricao = models.CharField(max_length=60, null=False)
    grau_conta = models.PositiveSmallIntegerField(null=False)
    conta_superior = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(999999)])

    # R= Receita C= Custos D= Despesas
    receita_despesa = models.CharField(max_length=1, null=False)

    data_inclusao = models.DateTimeField(auto_now=False)

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="S",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='N para bloquear esta NATUREZA DE CUSTOS financeiros para uso no sistema '
                                            'em todos os módulos')

    def __str__(self):
        return str(self.codigo) + " - "  + self.descricao

    class Meta:
        ordering = ('descricao',)
        verbose_name = 'Natureza de Custo'
        verbose_name_plural = 'Naturezas de Custo'


# ----------------------------------------------------------------------------------------------------------------------
# ARQUIVO CENTROS DE CUSTOS - TABELAS GENERICAS DO SISTEMA USESOFTR3
# (usesoft=KCCI55)
# ----------------------------------------------------------------------------------------------------------------------
class CentroCusto(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(99999)],
                                         help_text='Código do Centro de custos do sistema para uso em demonstrações '
                                                   'financeiras')
    descricao = models.CharField(max_length=60, null=False)
    ativo = models.BooleanField(default=True)
    data_inclusao = models.DateField(max_length=8, auto_now_add=True)
    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="S",
                                  choices=SIM_NAO_CHOICES, help_text='N para bloquear esta NATUREZA DE CUSTOS para '
                                                                     'uso no sistema em todos os módulos')

    def __str__(self):
        return str(self.codigo) + " - " + self.descricao

    class Meta:
        ordering = ('descricao', )
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custos'


# -----------------------------------------------------------------------------------------------------------------------
# TIPOS DE DOCUMENTO GERADO NO FINANCEIRO DOC, CHE, DUP, DIN, ETC
# -----------------------------------------------------------------------------------------------------------------------
class TipoDocumento(models.Model):
    codigo = models.CharField("Codigo tipo de documento", null=False, unique=True, max_length=3, default="DIN")

    descricao = models.CharField("Descrição tipo de documento", max_length=60, null=False, unique=True,
                                 help_text='Descrição tipo de documento para venda ou compra de produtos')

    habilitado_vendas = models.CharField("Habilitado em vendas", max_length=1, default="S", choices=SIM_NAO_CHOICES,
                                         help_text='N para bloquear esta forma de pagamento nas vendas, nas '
                                                   'confirmações de pedidos de clientes')

    habilitado_nfce = models.CharField("Habilitado para NFce/Cupom Fiscal", max_length=1, null=False, default="S",
                                       choices=SIM_NAO_CHOICES,
                                       help_text='N para bloquear esta forma de pagamento nas vendas diretas no caixa '
                                                 'em emissão de NFce')

    habilitado_web = models.CharField("Habilitado para Vendas Web", max_length=1, null=False, default="S",
                                      choices=SIM_NAO_CHOICES,
                                      help_text='S para bloquear esta forma de pagamento nas vendas via TABLET, '
                                                'Vendedores externos Web')

    tipo_documento = models.CharField("Tipo de documento para NFCe", max_length=60, null=False, default="S",
                                      choices=TIPO_DOCUMENTO_CHOICES,
                                      help_text='Tipo de documento para NFCe Dinheiro/Cheque/Cartão/Etc')

    indicador_pagamento_nfe = models.CharField("Indicador da forma de pagamento", max_length=1, null=False, default="0",
                                               choices=INDICADOR_PAGAMENTO_CHOICES,
                                               help_text='Indicador da forma de pagamento para informação na nota '
                                                         'fiscal eletrônica')

    # Natureza de custos deste tipo de operacao de venda ou para qual conta de custos sistema irá
    # TODO Depois excluir a opção null=True
    # natureza_custos = models.ForeignKey(NaturezaCusto, default=0, on_delete=models.CASCADE, blank=True, null=True)
    natureza_custos = models.PositiveIntegerField(null=True, blank=True, default=1)

    # Centro de custos deste tipo de operacao de venda ou para qual conta de custos sistema irá
    # TODO Depois excluir a opção null=True
    # centro_custos = models.ForeignKey(CentroCusto, default=0, on_delete=models.CASCADE, blank=True, null=True)
    centro_custos = models.PositiveIntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ('descricao',)
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'


# ----------------------------------------------------------------------------------------------------------------------
# TIPOS DE PAGAMENTOS EXISTENTES NO SISTEMA (KCEITP)
# ----------------------------------------------------------------------------------------------------------------------
class TipoPagamento(models.Model):
    codigo = models.CharField("Código Forma Pagamento", null=False, unique=True, max_length=3, default="DIN")
    descricao = models.CharField("Descrição Forma Pagamento", max_length=60, null=False, default=" ",
                                 help_text='Descrição Forma Pagamento para venda ou compra de produtos')
    habilitado = models.CharField("Tipo habilitado", max_length=60, null=False, default="S",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='S para bloquear esta forma de pagamento nas vendas')
    negociada = models.CharField("Pode haver negociação", max_length=60, null=False, default="S",
                                 choices=SIM_NAO_CHOICES, help_text='S para permitir que vendedor possa negociar a '
                                                                    'forma de pagamento com cliente N- Não negocia')
    venda_parcelada = models.CharField("Pode haver parcelamento", max_length=60, null=False, default="S",
                                       choices=SIM_NAO_CHOICES, help_text='S para permitir que vendedor possa '
                                                                          'parcelar venda N- Não parcela')
    imprime_na_nfe = models.CharField("Imprimir dados na nota fiscal", max_length=60, null=False, default="S",
                                      choices=SIM_NAO_CHOICES, help_text='S para permitir que sistema imprima os '
                                                                         'dados financeiros na nfe / Danfe')
    habilitado_web = models.CharField("Habilita forma de pagamento na WEB", max_length=60, null=False, default="N",
                                      choices=SIM_NAO_CHOICES, help_text='S Habilita forma de pagamento na vendas '
                                                                         'via site WEB')
    # número de parcelas pré determinado para este pagamento - Se zeros, força que seja a vista
    num_parcelas = models.PositiveIntegerField("Numero de parcelas", null=False,  validators=[MaxValueValidator(999)],
                                               help_text='Numero máximo de parcelas pre determinado para este '
                                                         'pagamento. Se zeros, força que seja a vista')
    prazos_padroes = models.CharField("Prazos padroes em dias", max_length=60, null=False, default="000",
                                      help_text='Informe os prazos padroes em numero de dias consecutivos de 3 em 3 '
                                                'ex 000030060090')

    # prazo em dias máximo pre determinado para este pagamento
    prazo_maximo = models.PositiveIntegerField("Prazo máximo em dias", null=False,  validators=[MaxValueValidator(999)],
                                               help_text='Número máximo de prazo em dias pre determinado para '
                                                         'este pagamento')

    # tipo de documento será gerado para este tipo de venda
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)

    # Valor mínimo para este tipo de pagamento reverse
    valor_minimo = models.DecimalField("Valor mínimo para venda", max_length=16, max_digits=16, decimal_places=2,
                                       default=0.00, help_text='Valor mínimo para este tipo de pagamento reverse')

    # Valor máximo para este tipo de pagamento reverse
    valor_maximo = models.DecimalField("Valor máximo para venda", max_length=16, max_digits=16, decimal_places=2,
                                       default=0.00, help_text='Valor máximo para este tipo de pagamento reverse')

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ('descricao',)
        verbose_name = 'Tipo de Pagamento'
        verbose_name_plural = 'Tipos de Pagamentos'


# ----------------------------------------------------------------------------------------------------------------------
# PRAZOS DE PAGAMENTOS EXISTENTES NO SISTEMA (KCEITP)
# ----------------------------------------------------------------------------------------------------------------------
class PrazoPagamento(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(99999)])
    descricao = models.CharField(max_length=60, null=False)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ('codigo', )
        verbose_name = 'Prazo de Pagamento'
        verbose_name_plural = 'Prazos de Pagamentos'
