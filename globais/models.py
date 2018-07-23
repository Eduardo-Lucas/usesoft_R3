from django.db import models

from django.core.validators import MaxValueValidator
from choices.models import SIM_NAO_CHOICES, CALCULA_CUSTOS_CFOP_CHOICES, OPERACAO_ICMS_CHOICES, OPERACAO_IPI_CHOICES, \
    FINALIDADE_CFOP_CHOICES, CALC_CUSTOS_CFOP_CHOICES, FINANCEIRO_CFOP_CHOICES


# ----------------------------------------------------------------------------------------------------------------------
# Mensagens padroes do sistema
# utilizada no faturamento, pedidos, produtos e CFOPs
# ----------------------------------------------------------------------------------------------------------------------
class MensagemPadrao(models.Model):
    codigo = models.CharField("Codigo da Mensagem Padrao", max_length=4, null=False, unique=True)
    descricao = models.CharField("Descrição do Mensagem?", max_length=2048, null=False,)

    habilitado = models.CharField("Habilitada para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite esta mensagem caso sua empresa não a utilize ou utilize muito '
                                            'esporadicamente para evitar erros')

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['codigo']
        unique_together = ('codigo', 'descricao')
        verbose_name = 'Mensagem Padrão'
        verbose_name_plural = 'Mensagens Padrões'


# ----------------------------------------------------------------------------------------------------------------------
# SituacaoTribIcms
# D:\DjangoProjects\usesoft_R3\tabelasglobais\CST_ICMS.txt
# ----------------------------------------------------------------------------------------------------------------------
class SituacaoTribIcms(models.Model):
    codigo = models.PositiveIntegerField("Código", validators=[MaxValueValidator(999)])
    descricao = models.CharField("Descrição", max_length=300, null=False)
    data_publicacao = models.DateField("Data de Publicação", null=True, blank=True)
    data_validade = models.DateField("Data de Validade", null=True, blank=True)

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="S",
                                  choices=SIM_NAO_CHOICES, help_text='Desabilite esta Situação Tributária caso sua '
                                                                     'empresa não o utilize ou utilize muito '
                                                                     'esporadicamente para evitar erros')

    def __str__(self):
        return str(self.codigo) + " - " + self.descricao

    class Meta:
        ordering = ['codigo']
        unique_together = ('codigo', 'descricao')
        verbose_name = 'Situação Tributária ICMS'
        verbose_name_plural = 'Situações Tributárias ICMS'


# ----------------------------------------------------------------------------------------------------------------------
# SituacaoTribIpi
# D:\DjangoProjects\usesoft_R3\tabelasglobais\CST_IPI.txt
# ----------------------------------------------------------------------------------------------------------------------
class SituacaoTribIpi (models.Model):
    codigo = models.PositiveIntegerField("Código", unique=True, validators=[MaxValueValidator(99)])
    descricao = models.CharField("Descrição", max_length=100, null=False)
    data_publicacao = models.DateField("Data de Publicação", null=True, blank=True)
    data_validade = models.DateField("Data de Validade", null=True, blank=True)
    habilitado = models.CharField("Habilitado para uso", max_length=1, default="S", choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite Situação Tributária caso sua empresa não o utilize ou utilize '
                                            'muito esporadicamente para evitar erros')

    def __str__(self):
        return str(self.codigo) + " - " + self.descricao

    class Meta:
        ordering = ['codigo']
        unique_together = ('codigo', 'descricao')
        verbose_name = 'Situação Tributária IPI'
        verbose_name_plural = 'Situações Tributárias IPI'


# ----------------------------------------------------------------------------------------------------------------------
# SituacaoTribPis
# D:\DjangoProjects\usesoft_R3\tabelasglobais\CST_PIS.txt
# ----------------------------------------------------------------------------------------------------------------------
class SituacaoTribPis(models.Model):
    codigo = models.PositiveIntegerField("Código", null=False, validators=[MaxValueValidator(99)])
    descricao = models.CharField("Descrição", max_length=200, null=False)
    data_publicacao = models.DateField("Data de Publicação", null=True, blank=True)
    data_validade = models.DateField("Data de Validade", null=True, blank=True)

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES, help_text='Desabilite este Situação Tributária caso sua '
                                                                     'empresa não o utilize ou utilize muito '
                                                                     'esporadicamente para evitar erros')

    def __str__(self):
        return str(self.codigo) + " - " + self.descricao

    class Meta:
        ordering = ['codigo']
        unique_together = ('codigo', 'descricao')
        verbose_name = 'Situação Tributária PIS'
        verbose_name_plural = 'Situações Tributárias PIS'


# ----------------------------------------------------------------------------------------------------------------------
# SituacaoTribCofins
# D:\DjangoProjects\usesoft_R3\tabelasglobais\CST_COFINS.txt
# ----------------------------------------------------------------------------------------------------------------------
class SituacaoTribCofins(models.Model):
    codigo = models.PositiveIntegerField(validators=[MaxValueValidator(99)])
    descricao = models.CharField(max_length=150, null=False)
    data_publicacao = models.DateField(null=True, blank=True)
    data_validade = models.DateField(null=True, blank=True)

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES, help_text='Desabilite este cst caso sua empresa não o '
                                                                     'utilize ou utilize muito esporadicamente para '
                                                                     'evitar erros')

    def __str__(self):
        return str(self.codigo) + " - " + self.descricao

    class Meta:
        ordering = ['codigo']
        unique_together = ('codigo', 'descricao')
        verbose_name = 'Situação Tributária COFINS'
        verbose_name_plural = 'Situações Tributárias COFINS'


# ----------------------------------------------------------------------------------------------------------------------
# TABELA SITUACAO TRIBUTARIA DO DOCUMENTO FISCAL
# D:\DjangoProjects\usesoft_R3\tabelasglobais\412 Tabela Situação do Documento.txt
# 00|Documento regular|01012009|
# 01|Documento regular extemporâneo|01012009|
# 02|Documento cancelado|01012009|
# 03|Documento cancelado extemporâneo|01012009|
# 04|NFe ou CT-e denegada|01012009|
# ----------------------------------------------------------------------------------------------------------------------
class SituacaoDocumentoSped(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(99)])
    descricao = models.CharField(null=False, max_length=100)
    data_validade = models.DateField(max_length=8, null=True, blank=True)

    def __str__(self):
        # ("%s is %d years old." % (name, age))
        return "%d - %s " % (self.codigo, self.descricao)

    class Meta:
        ordering = ('codigo',)
        verbose_name = 'Situação Documento Sped'
        verbose_name_plural = 'Situação Documentos Sped'


# ----------------------------------------------------------------------------------------------------------------------
# Código nacionais de municipios IBGE
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Municipios_Ibge.txt
# ----------------------------------------------------------------------------------------------------------------------
class Municipio(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(9999999)])
    descricao = models.CharField(max_length=80, null=False)
    data_publicacao = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.descricao + " - " + str(self.codigo)

    class Meta:
        ordering = ('descricao',)
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'


# ----------------------------------------------------------------------------------------------------------------------
# D:\DjangoProjects\usesoft_R3\tabelasglobais\UF_SIGLAS.txt
# AC|Acre|01012009|
# AL|Alagoas|01012009|
# AM|Amazonas|01012009|
# importar UF_BGE.txt com codigos e complementar com UF_SIGLAS.txt
# ----------------------------------------------------------------------------------------------------------------------
class Uf(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(99)])
    sigla_estado = models.CharField(max_length=2, null=False)
    estado = models.CharField(max_length=50, null=False)
    data_publicacao = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.codigo) + " - " + self.estado

    class Meta:
        ordering = ['sigla_estado']
        verbose_name = 'Unidade Federativa'
        verbose_name_plural = 'Unidades Federativas'


# ----------------------------------------------------------------------------------------------------------------------
# Código dos PAISES CONFORME IBGE
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Paises_IBGE.txt
# ----------------------------------------------------------------------------------------------------------------------
class PaisIbge(models.Model):
    codigo = models.PositiveIntegerField(null=False, unique=True, validators=[MaxValueValidator(9999)])
    descricao = models.CharField(max_length=60, null=False)
    data_publicacao = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.descricao + " - " + str(self.codigo)

    class Meta:
        ordering = ['descricao']
        verbose_name = 'País'
        verbose_name_plural = 'Países'


# ----------------------------------------------------------------------------------------------------------------------
# Código CNAE|Descrição do CNAE|
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Codigos_cnaes.txt
# ----------------------------------------------------------------------------------------------------------------------
class CodigoCnae(models.Model):
    codigo = models.CharField(unique=True, max_length=10, null=False)
    descricao = models.CharField(max_length=80, null=False)
    tipo_atividade = models.CharField(max_length=80, null=False)
    # true-cnae do simples False=Nao é do simples
    simples_nacional = models.BooleanField(default=False)
    per_imposto = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    # true-cnae precisa de inscricao estadual False=Nao precisa
    inscricao_estadual = models.BooleanField(default=False)

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ('descricao',)


# ----------------------------------------------------------------------------------------------------------------------
# TABELA DE TIPOS DE DOCUMENTOS FISCAIS
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Tabela Documentos Fiscais do ICMS.txt
# 55|Nota Fiscal Eletrônica|01012009|
# 57|Conhecimento de Transporte Eletrônico – CT-e|01012009|
# 59|Cupom Fiscal Eletrônico – CF-e|01062011|
# ----------------------------------------------------------------------------------------------------------------------
class ModeloDocumentoFiscal(models.Model):
    codigo = models.CharField(max_length=2, unique=True)
    descricao = models.CharField(max_length=100)
    data_validade = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.codigo + " - " + self.descricao

    class Meta:
        ordering = ('codigo',)
        verbose_name = 'Modelo de Documento Fiscal'
        verbose_name_plural = 'Modelos de Documentos Fiscais'


# ----------------------------------------------------------------------------------------------------------------------
# Tipo  movimentação no sistema de Estoques vinculado Aos CFOPs
# MV-Movimento Vendas / MC- Movimento Compra / BO-Bonificação
# ----------------------------------------------------------------------------------------------------------------------
class TipoOperacaoFiscal (models.Model):
    codigo = models.CharField("Tipo de Operação Fiscal?", max_length=4, null=False, unique=True)
    descricao = models.CharField("Descrição do Operação ou Movimento Fiscal na empresa?", max_length=50, null=False,)

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['codigo']
        unique_together = ('codigo', 'descricao')
        verbose_name = 'Tipo de Operação Fiscal'
        verbose_name_plural = 'Tipos de Operações Fiscais'


# ----------------------------------------------------------------------------------------------------------------------
# codigos fiscais de operação - CFOPs (kfai87)
# Tabela Global em  \DjangoProjects\usesoft_R3\TabelasGlobais\tb11966.txt
# versão=6 CFOP, DESC_CFOP, DT_INI, DT_FIM
# 1101|Compra para industrialização|01012009|
# 1102|Compra para comercialização|01012009|
# ----------------------------------------------------------------------------------------------------------------------
class Cfop(models.Model):
    codigo = models.PositiveIntegerField("Código CFOP", validators=[MaxValueValidator(9999)])
    descricao = models.CharField("Descrição do CFOP", max_length=512, blank=False)

    # Tipo de movimento fiscal - Vendas/Compras/bonificação/etc - usado no BI e outros relatorios de vendas
    # LEMBRAR que se tipo for uma TRANSFERÊNCIA (TR) sistema fará a transferência para a outra unidade modo automático
    tipomovimentofiscal = models.ForeignKey(TipoOperacaoFiscal, on_delete=models.CASCADE,
                                            help_text='Tipo de movimento fiscal - Vendas/Compras/bonificação/etc - '
                                                      'usado no BI e outros relatorios de vendas')

    # falta tabela global
    # 4.3.7 – Tabela Base de Cálculo do Crédito: SPED PIS COFINS
    # OBS: A ser utilizada na codificação da base de cálculo dos créditos apurado no
    # período, no caso de escrituração de registros referentes a documentos e operações
    # geradoras de crédito, nos Blocos A, C, D, F e 1 (Créditos extemporâneos).
    natureza_base_calc_cred_pis = models.CharField("Base de Cálculo do Crédito: SPED PIS COFINS", max_length=2,
                                                   blank=False)

    # mensagem padrao a ser impressa durante a emissão da nota fiscal como observações adicionais na NF
    mensagempadrao = models.ForeignKey(MensagemPadrao, on_delete=models.CASCADE,
                                       help_text='Mensagem padrão a ser impressa durante a emissão da nota fiscal '
                                                 'como observações adicionais na NF')

    dias_devolucao = models.PositiveIntegerField("Número de dias para Devolução", null=False,
                                                 validators=[MaxValueValidator(999)])
    pode_subst_tributaria = models.CharField("CFOP pode ter Substituição Tributária?", max_length=1, null=False,
                                             choices=SIM_NAO_CHOICES, default="N")

    tributado_icms = models.CharField("Calcular tributação de Icms?", max_length=1, null=False,
                                      choices=SIM_NAO_CHOICES, default="S")
    # "S" para que entradas deste CFOP possa existir crédito de ICMS (Ex compra revenda empresas lucro real/presumido)
    # "N" não deixará sistema creditar icms  (Ex entrada uso e consumo 1556 ou 2556)
    credito_icms = models.CharField("Pode ter crédidos de icms?", max_length=1, null=False, choices=SIM_NAO_CHOICES,
                                    default="S")
    reduz_base_icms = models.CharField("Pode ter redução de Base?", max_length=1, null=False, choices=SIM_NAO_CHOICES,
                                       default="S")
    #  tipo de OPERACAO FISCAL LIVROS FISCAIS (1,2,3)
    #  1. Operação com crédito de impostos
    #  2. Operação sem crédito de impostos - ISENTAS/NÃO TRIBUTADAS
    #  3. Operação sem crédito impostos - OUTRAS
    operacao_icms = models.CharField("Operação com ICMS nos Livros Fiscais", max_length=1, null=False,
                                     choices=OPERACAO_ICMS_CHOICES, default="1")

    tributado_ipi = models.CharField("Cfop tem tributação de IPI?", max_length=1, null=False,
                                     choices=SIM_NAO_CHOICES, default="S")
    credito_ipi = models.CharField("Permite Crédito de IPI?", max_length=1, null=False,
                                   choices=SIM_NAO_CHOICES, default="S")
    # 1. Operação com crédito de impostos  2. Operação sem crédito de impostos - ISENTAS/NÃO TRIBUTADAS
    # 3. Operação sem crédito - OUTRAS
    operacao_ipi = models.CharField("Operação com IPI nos Livros Fiscais", max_length=1, null=False,
                                    choices=OPERACAO_IPI_CHOICES, default="1")

    tributado_pis_cofins = models.CharField("Calcular tributação de Pis/Cofins?", max_length=1, null=False,
                                            choices=SIM_NAO_CHOICES, default="S")
    credito_pis_cofins = models.CharField("Permite Crédito de Pis/Cofins?", max_length=1, null=False,
                                          choices=SIM_NAO_CHOICES, default="S")

    # "S" para que este cfop seja colocado em todos os itens da NF
    # "N" para que este cfop seja livre escolha do usuario conforme configuração pedido
    cfop_padrao = models.CharField("Cfop é padrão em todos os itens?", max_length=1, null=False,
                                   choices=SIM_NAO_CHOICES, default="S")

    # "S" para informar que este CFOP movimentará o estoque fiscal
    # Lembrar que este campo será levado para o item da tabela de itens da NFe e poderá ser alterado
    movimenta_estoques = models.CharField("Cfop é padrão em todos os itens?", max_length=1, null=False,
                                          choices=SIM_NAO_CHOICES, default="S")

    # tipo de pagamento obrigatório para este cfop (bonificações a cobrar)
    #  "S - Financeiro obrigatório NF=PAGAR"
    #  "N - Financeiro NÃO é obrigatório na NF"
    #  "B - NFe não tem financeiro (Bonificação, etc)"
    #  "A - Apenas Avisa ao usuário "
    movimenta_financeiro = models.CharField("Financeiro na Nfe será obrigatório?", max_length=1, null=False,
                                            choices=FINANCEIRO_CFOP_CHOICES, default="S")

    # "S" para calcular custos na NFe de entrada "N" nao calculará custos
    calcula_custos = models.CharField("Calcular preços de Custos", max_length=1, null=False,
                                      choices=CALCULA_CUSTOS_CFOP_CHOICES, default="S")
    #  Nestes campos lembrar  "-" Credito - Subtrai valor do preco na nf (icm)
    #                         "+" Soma valor ao preco da NF (Ex. IPI)
    #                         "I" Ignora valor, nao soma nem subtrai
    custo_icms = models.CharField("Icms no Custo", max_length=1, null=False,
                                  choices=CALC_CUSTOS_CFOP_CHOICES, default="-")
    custo_ipi = models.CharField("Ipi no Custo", max_length=1, null=False,
                                 choices=CALC_CUSTOS_CFOP_CHOICES, default="+")
    custo_frete = models.CharField("Frete no Custo", max_length=1, null=False,
                                   choices=CALC_CUSTOS_CFOP_CHOICES, default="+")
    custo_icms_frete = models.CharField("Icms do Frete no Custo", max_length=1, null=False,
                                        choices=CALC_CUSTOS_CFOP_CHOICES, default="-")
    custo_pis = models.CharField("Pis no Custo", max_length=1, null=False,
                                 choices=CALC_CUSTOS_CFOP_CHOICES, default="-")
    custo_cofins = models.CharField("Cofins no Custo", max_length=1, null=False,
                                    choices=CALC_CUSTOS_CFOP_CHOICES, default="-")
    custo_seguro = models.CharField("Seguro no Custo", max_length=1, null=False,
                                    choices=CALC_CUSTOS_CFOP_CHOICES, default="+")
    custo_despesas = models.CharField("Despesas no Custo", max_length=1, null=False,
                                      choices=CALC_CUSTOS_CFOP_CHOICES, default="+")
    custo_descontos = models.CharField("Descontos no Custo", max_length=1, null=False,
                                       choices=CALC_CUSTOS_CFOP_CHOICES, default="-")
    custo_icms_sub = models.CharField("Icms Subs no Custo", max_length=1, null=False,
                                      choices=CALC_CUSTOS_CFOP_CHOICES, default="+")
    custo_antecipacao_trib = models.CharField("Icms Subs no Custo", max_length=1, null=False,
                                              choices=CALC_CUSTOS_CFOP_CHOICES, default="+")

    # 1_NF-e normal  "2_NF-e complementar  "3_NF-e de ajuste "4_NF-e Devolução/retorno "
    finalidade_nfe = models.CharField("Finalidade padrão na Emissão da NFe", max_length=1, null=False,
                                      choices=FINALIDADE_CFOP_CHOICES, default="+")

    # "S" para exigir do fiscal referenciado e  "N" nao exigirá
    doc_referenciado = models.CharField("Calcular preços de Custos", max_length=1, null=False,
                                        choices=SIM_NAO_CHOICES, default="+")

    def __str__(self):
        return str(self.codigo) + " - " + str(self.descricao)

    class Meta:
        ordering = ['descricao']
        verbose_name = 'CFOP'
        verbose_name_plural = 'CFOPs'


# ----------------------------------------------------------------------------------------------------------------------
# plano de contas referencial BACEN -
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Contas_referenciais_Bacen.txt
# ----------------------------------------------------------------------------------------------------------------------
class ContaReferencialBacen(models.Model):
    codigo_conta = models.CharField(unique=True, max_length=20, null=False)
    descricao = models.CharField(max_length=80, null=False)
    data_inicio = models.DateField(max_length=8)
    data_fim = models.DateField(max_length=8)
    tipo_conta = models.CharField(max_length=1)
    conta_superior = models.CharField(unique=True, max_length=20)
    nivel_contabil = models.PositiveSmallIntegerField()
    codigo_natureza = models.CharField(unique=True, max_length=1)
    utilizacao = models.CharField(unique=True, max_length=1)

    def __str__(self):
        return self.codigo_conta

    class Meta:
        ordering = ('descricao',)


# ----------------------------------------------------------------------------------------------------------------------
# plano de contas reverencial BACEN -
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Contas_referenciais_Dinamica.TXT
# ----------------------------------------------------------------------------------------------------------------------
class ContaReferencialDinamica(models.Model):
    codigo_conta = models.CharField(unique=True, max_length=20, null=False)
    descricao = models.CharField(max_length=80, null=False)
    data_inicio = models.DateField(max_length=8)
    data_fim = models.DateField(max_length=8)
    tipo_conta = models.CharField(max_length=1)
    conta_superior = models.CharField(unique=True, max_length=20)
    nivel_contabil = models.PositiveSmallIntegerField()
    codigo_natureza = models.CharField(unique=True, max_length=1)
    utilizacao = models.CharField(unique=True, max_length=1)

    def __str__(self):
        return self.codigo_conta

    class Meta:
        ordering = ('descricao',)


# ----------------------------------------------------------------------------------------------------------------------
# plano de contas reverencial Susep -
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Contas_referenciais_Susep.txt
# ----------------------------------------------------------------------------------------------------------------------
class ContaReferencialSusep(models.Model):
    codigo_conta = models.CharField(unique=True, max_length=20, null=False)
    descricao = models.CharField(max_length=80, null=False)
    data_inicio = models.DateField(max_length=8)
    data_fim = models.DateField(max_length=8)
    tipo_conta = models.CharField(max_length=1)
    conta_superior = models.CharField(unique=True, max_length=20)
    nivel_contabil = models.PositiveSmallIntegerField()
    codigo_natureza = models.CharField(unique=True, max_length=1)
    utilizacao = models.CharField(unique=True, max_length=1)

    def __str__(self):
        return self.codigo_conta

    class Meta:
        ordering = ('descricao',)


# ----------------------------------------------------------------------------------------------------------------------
# CodigoNcm
# D:\DjangoProjects\usesoft_R3\tabelasglobais\CodigoNCM.txt
# ----------------------------------------------------------------------------------------------------------------------
class CodigoNcm(models.Model):
    codigo = models.CharField(max_length=8, unique=True)
    unidade = models.CharField(max_length=10)
    data_publicacao = models.DateField()
    data_validade = models.DateField(null=True, blank=True)
    descricao_unidade = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo + " - " + self.unidade + " - " + self.descricao_unidade

    class Meta:
        ordering = ('codigo',)
        verbose_name = 'Código NCM'
        verbose_name_plural = 'Códigos NCM'


# ----------------------------------------------------------------------------------------------------------------------
# CodigoCest
# D:\DjangoProjects\usesoft_R3\tabelasglobais\Cest Substituicao Tributaria.txt
# ----------------------------------------------------------------------------------------------------------------------
class CodigoCest(models.Model):
    codigo = models.CharField("Código", max_length=7)
    descricao = models.CharField("Descrição", max_length=350)
    data_inicio = models.DateField("Data de Início")
    data_fim = models.DateField("Data Fim", blank=True, null=True)

    def __str__(self):
        return self.codigo + " - " + self.descricao

    class Meta:
        ordering = ('codigo',)
        verbose_name = 'Código CEST'
        verbose_name_plural = 'Códigos CEST'


# ----------------------------------------------------------------------------------------------------------------------
# CodigoNbs
# D:\DjangoProjects\usesoft_R3\tabelasglobais\NOMENCLATURA_BRASILEIRA_DE_SERVICOS.xls
# ----------------------------------------------------------------------------------------------------------------------
class CodigoNbs(models.Model):
    codigo = models.CharField(max_length=7)
    descricao = models.CharField(max_length=100)

    class Meta:
        ordering = ('codigo',)
        verbose_name = 'Código NBS'
        verbose_name_plural = 'Códigos NBS'
