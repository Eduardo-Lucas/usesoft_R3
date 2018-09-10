# coding=utf-8
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from choices.models import INDICADOR_PAGAMENTO_CHOICES, STATUS_PEDIDO_ITEM_CHOICES, REGIME_TRIBUTARIO_CHOICES, \
    EMISSAO_CHOICES, INDICA_PRESENCA_CHOICES, INDICADOR_FRETE_CHOICES, TIPO_FRETE_CHOICES, \
    STATUS_CONFERENCIA_CHOICES, SIM_NAO_CHOICES, MODALIDADE_IPI_CHOICES, MODALIDADE_CALC_ICMS_CHOICES, \
    MODALIDADE_ICMS_CHOICES, STATUS_DIFERENCA_CHOICES, MODALIDADE_ICMSSUB_CHOICES, TIPO_PRECO_CHOICES, \
    INDICA_NFCE_CHOICES, ALTERA_PRECOS_CHOICES, TRANSFERENCIA_CHOICES, TIPO_ENTREGA_CHOICES, ESCOLHE_DESCONTO_CHOICES, \
    MODALIDADE_PAUTA_CHOICES, MOTIVO_DESONERACAO_ICM_CHOICES, MULTIPLICA_DIVIDE_CHOICES, TIPO_CODIGO_CHOICES, \
    quantidade_maior_que_zero
from financeiro.models import NaturezaCusto, CentroCusto, TipoPagamento, PrazoPagamento
from globais.models import MensagemPadrao, Cfop, SituacaoTribIcms, SituacaoTribPis, SituacaoTribCofins, \
    SituacaoTribIpi, SituacaoDocumentoSped, ModeloDocumentoFiscal, TipoOperacaoFiscal, CodigoNcm, CodigoCest, Uf
from faturamento.models import Participante, NotaFiscal


def percentual_maximo_desconto(value):
    if float(int(value)) > 30:
        raise ValidationError(
            'O Percentual de Desconto NÃO PODE SER MAIOR que 30%.',
            params={'value': value},
        )


# ----------------------------------------------------------------------------------------------------------------------
# Tipo  de entrada e saida para efeito de diversas caracterizações de movimentos no estoque/materiais
# ----------------------------------------------------------------------------------------------------------------------
class PedidoTipo (models.Model):
    codigo = models.CharField("Tipo de Movimento Entrada/Saida", max_length=4, null=False, unique=True)
    descricao = models.CharField("Descrição tipo Movimento Entrada/Saida", max_length=60, null=False)

    # lembrar que este tipo de operação fiscal deverá estar configurado no tipo de movimento de entrada ou saida
    # venda uso e consumo, transferência, ativo
    tipooperacaofiscal = models.ForeignKey(TipoOperacaoFiscal, on_delete=models.CASCADE,
                                           help_text='Tipo de movimento fiscal nesta operação conforme tipo de CFOP - '
                                                     'TT para todas as operações fiscais')

    # Tipo de Preço usado na saida de pedidos V Preço VENDA / C Último CUSTO / I Preço indexado, etc
    tipo_preco_pedido = models.CharField("Tipo de preço utilizar no pedido", max_length=1, null=False,
                                         choices=TIPO_PRECO_CHOICES,
                                         help_text='Tipo de Preço usado na saida de pedidos V Preço VENDA / C Último '
                                                   'CUSTO / I Preço indexado, etc')

    # percentual para mais ou para menos para ser acrescido/diminuido nas saidas de pedidos
    per_preco = models.DecimalField(max_length=7, max_digits=7, decimal_places=4, default=0.00,
                                    help_text='percentual para mais ou para menos para ser acrescido/diminuido nas '
                                              'saidas de pedidos.')

    # indPres (nfe 3.10) Indicador de presença do comprador no estabelecimento comercial no momento da operação NFe
    indicador_presenca_nfe = models.CharField("Indicador de presença do comprador NFe", max_length=1, null=False, 
                                              choices=INDICA_PRESENCA_CHOICES, default="1", 
                                              help_text='indPres (nfe 3.10) Indicador de presença do comprador no '
                                                        'estabelecimento comercial no momento da operação')

    # indPres (nfe 3.10) Indicador de presença do comprador no estabelecimento comercial no momento da operação NFCe
    indicador_presenca_nfce = models.CharField("Indicador de presença do comprador NCFe", max_length=1, null=False,
                                               choices=INDICA_NFCE_CHOICES, default="1",
                                               help_text='indPres (nfe 3.10) Indicador de presença para NFCe no '
                                                         'momento da operação')

    # Mensagem padrao a ser levada com observações na emissão do pedido e/ou como observações adicionais na NF
    mensagem_padrao = models.ForeignKey(MensagemPadrao,
                                        on_delete=models.CASCADE, help_text='Mensagem padrao a ser levada com '
                                                                            'observações na emissão do pedido e/ou '
                                                                            'como observações adicionais na NF')

    # Natureza de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    natureza_custos = models.ForeignKey(NaturezaCusto, default=1, on_delete=models.CASCADE)

    # Centro de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    centro_custo = models.ForeignKey(CentroCusto, default=1, on_delete=models.CASCADE)

    # Informe o Cfop para esta operação caso queira que sistema leve cfop para itens da NFe
    cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE)

    # Permite informar orçamentos somente com cabeçalho ou com quantidade zerada nos produtos
    quantidade_zero = models.CharField("Permite produtos com quantidade zero?", max_length=1, null=False,  default="N",
                                       choices=SIM_NAO_CHOICES,
                                       help_text='Permite informar orçamentos somente com cabeçalho ou com quantidade'
                                                 ' zerada nos produtos')

    altera_precos = models.CharField("Pode alterar preços nos produtos do pedido?", max_length=1, null=False,
                                     default="U", choices=ALTERA_PRECOS_CHOICES,
                                     help_text='S ou N para permitir alterar preços nos produtos do pedido?')

    # T - Transferência p/ Filial / O - Transferência p/outra empresa / N - Não é transferencia
    transferencia = models.CharField("Pedido é uma transferência?", max_length=1, null=False, default="N",
                                     choices=TRANSFERENCIA_CHOICES,
                                     help_text='T, O para permitir transferir e dar entrada automática na outra unidade'
                                               ' de negócio')

    # Tipo de pagamento deste pedido
    tipo_de_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.CASCADE, default=1,
                                          related_name='tipopagamentoTipo')

    # Prazo para pagamento deste pedido
    prazo_de_pagamento = models.ForeignKey(PrazoPagamento, on_delete=models.CASCADE)

    # Tipo de entrega Ex: 1 Cliente Compra produtos e leva/Transporta da Loja
    tipo_entrega = models.CharField("Pedido é uma transferencia?", max_length=1, null=False, default="1",
                                    choices=TIPO_ENTREGA_CHOICES,
                                    help_text='Tipo de entrega Ex: 1 Cliente Compra produtos e leva/Transporta da Loja')

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['codigo'] 
        verbose_name = 'Tipo de Pedido'
        verbose_name_plural = 'Tipos de Pedidos'


# ----------------------------------------------------------------------------------------------------------------------
# Tipo  de entrada e saida para efeito de diversas caracterizações de movimentos no estoque/materiais
# ----------------------------------------------------------------------------------------------------------------------
class ProdutoPromocao (models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    descricao = models.CharField("Descrição da promoção", max_length=60, null=False)

    data_movimento = models.DateTimeField('Data limite desta promoção', null=False, blank=False,
                                          help_text='Data limite desta promoção. Quando chegar a esta data e hora esta'
                                                    ' promoção será automaticamente cancelada')

    disponivel_para_venda = models.DecimalField("Quantidade disponível", max_length=16, max_digits=16, decimal_places=4,
                                                default=0.00,
                                                help_text='Saldo disponível para esta promoção. Quando saldo atingir '
                                                          'quantidade abaixo desta quantidade item sai da promoção')

    desconto = models.DecimalField("percentual de desconto no Preço de venda", max_length=8, max_digits=8,
                                   decimal_places=4, default=0.00,
                                   help_text='Percentual de desconto no preço de venda durante as vendas de modo '
                                             'automático')

    mostra_desconto = models.CharField("Mostrar % de desconto durante a venda", max_length=1, null=False, default="M",
                                       choices=ESCOLHE_DESCONTO_CHOICES,
                                       help_text='M para mostrar o % de desconto durante a venda e L para calcular '
                                                 'valor líquido e mostar somente total líquido')

    produto_bonificacao = models.CharField("Código do produto a bonificar nesta promoção", max_length=1, null=False,
                                           default="N",
                                           help_text='Código do produto a bonificar nesta promoção, quando vender '
                                                     'produto em promoção bonificar este codigo')

    quantidade_bonificacao = models.DecimalField("Quantidade bonificar neste promoção", max_length=16, max_digits=16,
                                                 decimal_places=4, default=0.00,
                                                 help_text='Quantidade do produtos a bonificar que será colocada no '
                                                           'pedido automaticamente durante a venda com valor zeros ou'
                                                           ' desconto de 99,9999%')

    def __str__(self):
        return str(self.produto) + " - " + self.descricao

    class Meta:
        ordering = ['produto']
        verbose_name = 'Promoção de Produto'
        verbose_name_plural = 'Promoções de Produtos'


# -----------------------------------------------------------------------------------------------------------------------
# localizações no depósito
# -----------------------------------------------------------------------------------------------------------------------
class ProdutoLocalizacao(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    codigo = models.CharField("Código do grupo", max_length=13, null=False, unique=True,
                              help_text='Código da localização dos produtos para efeito de armazenagem')

    descricao = models.CharField("Descrição do grupo", max_length=60, null=False, default=" ",
                                 help_text='Descrição do grupo de produtos')

    capacidade = models.DecimalField("Capacidade máxima de armazenagem", max_length=16, max_digits=16, decimal_places=4,
                                     default=0.00,
                                     help_text='Capacidade máxima de armazenagem deste local para efeito de gestão '
                                               'de armazém')

    unidade = models.CharField("Unidade de armazenagem (Kg, mt, cx, fd, etc)", max_length=60, null=False, default=" ",
                               help_text='Unidade de armazenagem (Kg, mt, cx, fd, etc)')

    quantidade_armazenada = models.DecimalField("Quantidade armazenada neste local", max_length=16, max_digits=16,
                                                decimal_places=4, default=0.00,
                                                help_text='Quantidade armazenada deste local para efeito de gestão de'
                                                          ' armazém')

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="S",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite este GRUPO caso sua empresa não a utilize ou utilize muito '
                                            'esporadicamente para evitar erros')


# -----------------------------------------------------------------------------------------------------------------------
# Cadastro de grupos de produtos
# -----------------------------------------------------------------------------------------------------------------------
class ProdutoGrupo(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    codigo = models.CharField("Código do grupo", max_length=13, null=False, unique=True,
                              help_text='Código da grupo de produtos para efeito de diversas classificações')
    descricao = models.CharField("Descrição do grupo", max_length=60, null=False, default=" ",
                                 help_text='Descrição do grupo de produtos')

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="S",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite este GRUPO caso sua empresa não a utilize ou utilize muito '
                                            'esporadicamente para evitar erros')

    # mensagem a ser apresentada para usuario durante das vendas de produtos deste grupo
    mensagempadrao = models.ForeignKey(MensagemPadrao, on_delete=models.CASCADE)

    # desconto maximo no grupo de mercadorias deste grupo lembrar que todos os itens deste grupo serão alterados
    desconto_maximo = models.DecimalField("Desconto máximo nas vendas", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='desconto máximo no grupo de mercadorias deste grupo lembrar que '
                                                    'todos os itens deste grupo serão alterados')

    bloquear_compra = models.CharField("Bloquear Compras", max_length=1, null=False, default="N",
                                       choices=SIM_NAO_CHOICES,
                                       help_text='"S" para bloquear itens deste grupo nas compras a fornecedores quando'
                                                 ' da emissão do mapa de compras')

    bloquear_compra_web = models.CharField("Desabilitar produtos na Web", max_length=1, null=False, default="N",
                                           choices=SIM_NAO_CHOICES,
                                           help_text='"S" Desabilitar publicação de produtos na Web')

    # Lembrar que haverá uma sequência lógica para o cálculo conforme discriminado no cadastro do vendedor
    comissao_venda = models.DecimalField("Comissão do vendedor", max_length=8, max_digits=8, decimal_places=4,
                                         default=0.00,
                                         help_text='Comissão do vendedor a ser paga pelas vendas dos produtos deste '
                                                   'grupo')
    lucro_liquido = models.DecimalField("Lucro líquido para produtos deste grupo", max_length=8, max_digits=8,
                                        decimal_places=4, default=0.00,
                                        help_text='percentual de lucro líquido para mercadorias do grupo a ser '
                                                  'calculado durante as entradas de XMLs')
    custo_operacional = models.DecimalField("Custo operacional Fixo", max_length=8, max_digits=8, decimal_places=4,
                                            default=0.00,
                                            help_text='custo fixo operacional para o grupo de mercadorias de XMLs')
    pis = models.DecimalField("% de imposto para PIS", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                              help_text='% de imposto para PIS')
    cofins = models.DecimalField("% de imposto para cofins", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                                 help_text='% de imposto para cofins')
    icms = models.DecimalField("% de imposto para Icms", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                               help_text='% de imposto para Icms')
    outros_custos = models.DecimalField("% outros custos ", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                                        help_text='% outros custos incidentes no cálculo do preço de venda')
    markup = models.DecimalField("% de Markup a aplicar sobre o custo", max_length=8, max_digits=8, decimal_places=4,
                                 default=0.00, help_text='% de Markup a aplicar sobre o custo')
    # limites de descontos para abater ou aumentar a comissao do vendedor assumir primeiro por Vendedor sobre o Grupo
    #  se existir
    desc_01_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_01_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_01 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_02_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_02_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_02 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_03_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_03_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_03 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_04_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_04_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_04 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_05_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_05_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_05 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_06_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_06_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_06 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')


# -----------------------------------------------------------------------------------------------------------------------
# Cadastro de departamentos de produtos
# -----------------------------------------------------------------------------------------------------------------------
class ProdutoDepartamento(models.Model):
    codigo = models.CharField("Código do departamento", max_length=13, null=False, unique=True,
                              help_text='Código da departamento de produtos para efeito de diversas classificações')
    descricao = models.CharField("Descrição do departamento", max_length=60, null=False, default=" ",
                                 help_text='Descrição do departamento de produtos')

    # mensagem a ser apresentada para usuario durante das vendas de produtos deste departamento
    mensagempadrao = models.ForeignKey(MensagemPadrao, on_delete=models.CASCADE)

    # desconto máximo no departamento de mercadorias deste departamento lembrar que todos os itens deste departamento 
    # serão alterados
    desconto_maximo = models.DecimalField("Desconto máximo nas vendas", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='desconto maximo no departamento de mercadorias deste departamento'
                                                    ' lembrar que todos os itens deste departamento serão alterados')

    bloquear_compra = models.CharField("Bloquear Compras", max_length=1, null=False, default="N",
                                       choices=SIM_NAO_CHOICES,
                                       help_text='"S" para bloquear itens deste departamento nas compras a '
                                                 'fornecedores quando da emissão do mapa de compras')

    bloquear_compra_web = models.CharField("Desabilitar produtos na Web", max_length=1, null=False, default="N",
                                           choices=SIM_NAO_CHOICES,
                                           help_text='"S" Desabilitar publicação de produtos na Web')

    # Lembrar que haverá uma sequência lógica para o cálculo conforme discriminado no cadastro do vendedor
    comissao_venda = models.DecimalField("Comissão do vendedor", max_length=8, max_digits=8, decimal_places=4,
                                         default=0.00,
                                         help_text='Comissão do vendedor a ser paga pelas vendas dos produtos deste '
                                                   'departamento')
    lucro_liquido = models.DecimalField("Lucro líquido para produtos deste departamento", max_length=8, max_digits=8,
                                        decimal_places=4, default=0.00,
                                        help_text='percentual de lucro líquido para mercadorias do departamento a ser'
                                                  ' calculado durante as entradas de XMLs')
    custo_operacional = models.DecimalField("Custo operacional Fixo", max_length=8, max_digits=8, decimal_places=4,
                                            default=0.00, help_text='custo fixo operacional para o departamento de '
                                                                    'mercadorias de XMLs')
    pis = models.DecimalField("% de imposto para pis", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                              help_text='% de imposto para pis')
    cofins = models.DecimalField("% de imposto para cofins", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                                 help_text='% de imposto para cofins')
    icms = models.DecimalField("% de imposto para Icms", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                               help_text='% de imposto para Icms')
    outros_custos = models.DecimalField("% outros custos ", max_length=8, max_digits=8, decimal_places=4, default=0.00,
                                        help_text='% outros custos incidentes no cálculo do preço de venda')
    markup = models.DecimalField("% de Markup a aplicar sobre o custo", max_length=8, max_digits=8, decimal_places=4,
                                 default=0.00, help_text='% de Markup a aplicar sobre o custo')

    # limites de descontos para abater ou aumentar a comissao do vendedor assumir primeiro por Vendedor sobre o 
    # departamento se existir
    desc_01_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_01_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_01 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_02_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_02_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_02 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_03_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_03_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_03 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_04_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_04_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_04 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_05_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_05_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_05 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    desc_06_desde = models.DecimalField("% de acréscimo/desconto inicial", max_length=8, max_digits=8, decimal_places=4,
                                        default=0.00,
                                        help_text='% limite inicial do intervalo de acréscimos ou descontos que '
                                                  'vendedor poderá dar nos produtos deste grupo')
    desc_06_ate = models.DecimalField("% de acréscimo/desconto final", max_length=8, max_digits=8, decimal_places=4,
                                      default=0.00,
                                      help_text='% limite final do intervalo de acréscimos ou descontos que vendedor '
                                                'poderá dar nos produtos deste grupo')
    somar_abater_06 = models.DecimalField("% somar ou abater da comissão", max_length=8, max_digits=8, decimal_places=4,
                                          default=0.00,
                                          help_text='% somar ou abater da comissão nos produtos se vendedor der '
                                                    'desconto ou aumentar preços')

    def __str__(self):
        return "Id.: " + str(self.id) + "==>" + self.codigo + " - " + self.descricao

    class Meta:
        ordering = ['descricao']


# -----------------------------------------------------------------------------------------------------------------------
# Código de cores DO PRODUTO
# -----------------------------------------------------------------------------------------------------------------------
class ProdutoCor(models.Model):
    codigo = models.CharField("Código da COR", max_length=4, null=False, unique=True)
    descricao = models.CharField("Descrição da COR padrão do produto?", max_length=50, null=False, )

    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite este código caso sua empresa não utilize ou utilize muito '
                                            'esporadicamente para evitar erros')

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['codigo']


# -----------------------------------------------------------------------------------------------------------------------
# Código de tamanho da grade de itens
# -----------------------------------------------------------------------------------------------------------------------
class ProdutoTamanho(models.Model):
    codigo = models.CharField("Código do Tamanho Padrao", max_length=4, null=False, unique=True)
    descricao = models.CharField("Descrição do Tamanho?", max_length=50, null=False, )

    habilitado = models.CharField("Habilitada para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite este código caso sua empresa não utilize ou utilize muito '
                                            'esporadicamente  para evitar erros')

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['codigo']


# -----------------------------------------------------------------------------------------------------------------------
# Código de densidade da grade de itens
# -----------------------------------------------------------------------------------------------------------------------
class ProdutoDensidade(models.Model):
    codigo = models.CharField("Código da Densidade do produtos", max_length=4, null=False, unique=True)
    descricao = models.CharField("Descrição do Densidade?", max_length=50, null=False, )
    densidade_m3 = models.DecimalField("Densidade do produto por metro cubico", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='Densidade do produto em quilograma por metro cubico para efeito de '
                                                 'cálculos na produção')
    habilitado = models.CharField("Habilitada para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES, help_text='Desabilite este código caso sua empresa não '
                                                                     'utilize ou utilize muito esporadicamente '
                                                                     'para evitar erros')

    def __str__(self):
        return str(self.descricao)

    class Meta:
        ordering = ['codigo']


# ----------------------------------------------------------------------------------------------------------------------
# Cadastro de Categorias de Produtos
# ----------------------------------------------------------------------------------------------------------------------
class Categoria(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Categoria de Produto'
        verbose_name_plural = 'Categorias de Produtos'

    def __str__(self):
        return str(self.id) + "-" + self.nome

    def save(self):
        self.slug = slugify(self.nome)
        super(Categoria, self).save()

    def get_absolute_url(self):
        return reverse('materiais:produto_list_by_category', args=[self.slug])


# ----------------------------------------------------------------------------------------------------------------------
# Cadastro de produtos para venda
# Chaves necessárias (fabricante+descrição) (descrição)
# ----------------------------------------------------------------------------------------------------------------------
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    disponivel = models.CharField("Item Disponível?", max_length=1, choices=SIM_NAO_CHOICES, default='S')
    # produto = models.CharField("Código do produto", max_length=13, null=False, unique=True,
    #                           help_text='Código da mercadoria/ produto para produção ou venda')

    # TODO Nome mais apropriado deveria ser codigo
    produto = models.CharField("Código do produto", max_length=13, null=False)
    descricao = models.CharField("Descrição do produto", max_length=60, null=False, default=" ",
                                 help_text='Descrição do produto para venda ou produção')
    slug = models.SlugField(max_length=200, db_index=True, default=' ')
    image = models.ImageField(upload_to='produtos/%Y/%m/%d', blank=True)
    aplicacao = models.CharField("Aplicação do produto", max_length=60, null=False, default="geral",
                                 help_text='Aplicação/composição do produto para venda ou produção')
    unidade = models.CharField("Unidade de venda do produto", max_length=13, null=False, default="UN",
                               help_text='Unidade do produto vendido conforme cadastro no momento da venda. '
                                         'Unidade de venda')
    num_decimais = models.PositiveIntegerField("Número do decimais", null=False, default=0,
                                               validators=[MaxValueValidator(9)],
                                               help_text='Máscara de Número de decimais a utilizar durante as '
                                                         'operações')

    # TODO Depois excluir a opção null=True
    # tributacao_produto = models.ForeignKey(ProdutoTributacao, on_delete=models.CASCADE, blank=True, null=True)
    tributacao_produto = models.IntegerField(blank=True, null=True, default=0)

    # TODO Depois excluir a opção null=True
    codigo_ncm = models.ForeignKey(CodigoNcm, on_delete=models.CASCADE, blank=True, null=True)
    # codigo_ncm = models.IntegerField(blank=True, null=True, default=0)

    # TODO Depois excluir a opção null=True
    # codigo_cest = models.ForeignKey(CodigoCest, on_delete=models.CASCADE, blank=True, null=True)
    codigo_cest = models.IntegerField(blank=True, null=True, default=0)

    # TODO Depois excluir a opção null=True
    # codigo_nbs = models.ForeignKey(CodigoNbs, on_delete=models.CASCADE, blank=True, null=True)
    codigo_nbs = models.IntegerField(blank=True, null=True, default=0)

    # Fabricante ou fornecedor do produto
    # TODO Depois excluir a opção null=True
    # fabricante = models.ForeignKey(Participante, on_delete=models.CASCADE, blank=True, null=True)
    fabricante = models.IntegerField(blank=True, null=True, default=0)

    # Código do grupo deste produto para efeito de classificação interna
    # TODO Depois excluir a opção null=True
    # grupo = models.ForeignKey(ProdutoGrupo, on_delete=models.CASCADE, blank=True, null=True)
    grupo = models.IntegerField(blank=True, null=True, default=0)

    # Código do departamento onde produto está alocado para efeito de classificação interna
    # TODO Depois excluir a opção null=True
    # departamento = models.ForeignKey(ProdutoDepartamento, on_delete=models.CASCADE, blank=True, null=True)
    departamento = models.IntegerField(blank=True, null=True, default=0)

    preco_venda = models.DecimalField("Preço unitário  de venda", max_length=16, max_digits=16, decimal_places=2)

    # Aspectos promocionais e de estoques
    saldo_negativo = models.CharField("Aceita Saldo Fisico Negativo", max_length=1, null=False, default="N",
                                      choices=SIM_NAO_CHOICES,
                                      help_text='S para aceitar saldo negativo durante a venda e N para não aceitar')
    saldo_fiscal_negativo = models.CharField("Aceita Saldo Fiscal Negativo ", max_length=1, null=False, default="N",
                                             choices=SIM_NAO_CHOICES,
                                             help_text='S para aceitar saldo fiscal negativo durante a emissão das '
                                                       'notas fiscais e N para não aceitar')

    # Localização deste item no depósito  ou na loja
    # TODO Depois excluir a opção null=True
    # localizacao_deposito = models.ForeignKey(ProdutoLocalizacao, on_delete=models.CASCADE, blank=True, null=True)
    localizacao_deposito = models.IntegerField(blank=True, null=True)

    # embalagem de venda
    embalagem_venda = models.CharField("Embalagem de venda", max_length=15, null=False, default="UN",
                                       help_text='Embalagem de venda diferenciada da unidade de venda. Pode-se vender '
                                                 'UNI e embalar em caixa')

    embalagem_compra = models.CharField("Embalagem de venda", max_length=15, null=False, default="N",
                                        help_text='Embalagem de venda diferenciada da unidade de venda. Pode-se vender '
                                                  'UNI e embalar em caixa')

    quantidade_por_embalagem = models.DecimalField("Quantidade por embalagem", max_length=16, max_digits=16,
                                                   decimal_places=6, default=0.00,
                                                   help_text='Quantidade por embalagem de compra para efeito de '
                                                             'conversão na hora da entrada da NFe')

    multiplica_divide = models.CharField("Multiplica ou divide na NF entrada", max_length=1, null=False, default="N",
                                         choices=MULTIPLICA_DIVIDE_CHOICES,
                                         help_text='X para multiplicar a quantidade de entrada pela quantidade por '
                                                   'embalagem e / para dividir na entrada')

    peso_liquido = models.DecimalField("Peso líquido do produto", max_length=16, max_digits=16, decimal_places=6,
                                       default=0.00,
                                       help_text='Peso líquido para efeito de formação de carga e na emissão da  NFe')
    peso_bruto = models.DecimalField("Peso bruto do produto", max_length=16, max_digits=16, decimal_places=6,
                                     default=0.00,
                                     help_text='Peso bruto para efeito de formação de carga e na emissão da  NFe')

    largura = models.DecimalField("Largura  do produto em Metros", max_length=16, max_digits=16, decimal_places=6,
                                  default=0.00, help_text='Largura do produto em Metros')
    altura = models.DecimalField("altura do produto em Metros", max_length=16, max_digits=16, decimal_places=6,
                                 default=0.00, help_text='altura do produto em Metros')
    comprimento = models.DecimalField("comprimento do produto em Metros", max_length=16, max_digits=16,
                                      decimal_places=6, default=0.00, help_text='comprimento do produto em Metros')

    largura_palet = models.DecimalField("Largura do palet em Metros", max_length=16, max_digits=16, decimal_places=6,
                                        default=0.00, help_text='Largura do palet em Metros')
    altura_palet = models.DecimalField("altura do palet em Metros", max_length=16, max_digits=16, decimal_places=6,
                                       default=0.00, help_text='altura do palet em Metros')
    comprimento_palet = models.DecimalField("comprimento do palet em Metros", max_length=16, max_digits=16,
                                            decimal_places=6, default=0.00, help_text='palet do produto em Metros')
    peso_liquido_palet = models.DecimalField("Peso líquido do palet", max_length=16, max_digits=16, decimal_places=6,
                                             default=0.00, help_text='Peso líquido do palet para efeito de formação de '
                                                                     'carga e na emissão da  NFe')
    peso_bruto_palet = models.DecimalField("Peso bruto do palet", max_length=16, max_digits=16, decimal_places=6,
                                           default=0.00, help_text='Peso bruto do palet para efeito de formação de '
                                                                   'carga e na emissão da  NFe')
    quantidade_produtos_palet = models.DecimalField("Quantidade de produtos por palet", max_length=16, max_digits=16,
                                                    decimal_places=6, default=0.00, help_text='Quantidade de produtos '
                                                                                              'por palet')

    # cor deste produto na grade
    # TODO Depois excluir a opção null=True
    codigo_cor = models.ForeignKey(ProdutoCor, on_delete=models.CASCADE, blank=True, null=True,
                                   help_text='Código da cor deste produto')
    # tamanho
    # TODO Depois excluir a opção null=True
    codigo_tamanho = models.ForeignKey(ProdutoTamanho, on_delete=models.CASCADE, blank=True, null=True,)
    # densidade
    # TODO Depois excluir a opção null=True
    codigo_densidade = models.ForeignKey(ProdutoDensidade, on_delete=models.CASCADE, blank=True, null=True,)
    ultima_alteracao = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ['descricao', 'id']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.produto + " - " + self.descricao

    def save(self):
        self.slug = slugify(self.descricao)
        super(Produto, self).save()

    def get_absolute_url(self):
        return reverse('materiais:produto_detail', args=[self.id, self.slug])


# ----------------------------------------------------------------------------------------------------------------------
# Cadastro de tributações do produto - antigo kcei01j
# ----------------------------------------------------------------------------------------------------------------------
class ProdutoTributacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    estado = models.ForeignKey(Uf, on_delete=models.CASCADE)

    # lembrar que este tipo de operação fiscal deverá estar configurado no tipo de movimento de entrada ou saida
    # venda uso e consumo, venda normal, etc
    tipooperacaofiscal = models.ForeignKey(TipoOperacaoFiscal, on_delete=models.CASCADE)

    modalidade_calculo_subst = models.CharField("Modalidade de cálculo da base Icms Substituído ?", max_length=1,
                                                null=False,  default="3", choices=MODALIDADE_ICMSSUB_CHOICES,
                                                help_text='Modalidade de cálculo da base Icms Substituído')

    # natureza da operação fiscal de base  ou cfop que indicará o tipo de operação
    cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE, related_name='cfop')

    # percentual de icms pago na venda da mercadoria para este estado e cfop em conjunto
    perc_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                    help_text='Percentual do ICMS a recolher.')

    perc_reducao_icms = models.DecimalField("Percentual de redução de base do ICMS", max_length=10, max_digits=10,
                                            decimal_places=6, default=0.00,
                                            help_text='Percentual de redução de base do ICMS')

    # percentual de icms substituição tributária para cálculo do lucro valor sobre o qual será tributado
    perc_mva = models.DecimalField("Percentual do MVA Substituição", max_length=10, max_digits=10, decimal_places=6,
                                   default=0.00,
                                   help_text='Percentual do MVA substituição tributária.')

    #  percentual de icms substituição tributária p/cálculo do icm substituído
    perc_icms_sub = models.DecimalField("Percentual do ICMS substituição", max_length=10, max_digits=10,
                                        decimal_places=6, default=0.00,
                                        help_text='Percentual do ICMS substituição tributária total a recolher.')

    perc_reducao_icms_sub = models.DecimalField("Percentual de redução do Icms substituição", max_length=10,
                                                max_digits=10, decimal_places=6, default=0.00,
                                                help_text='Percentual de redução do Icms substituição')

    situacao_tributaria_icms = models.PositiveIntegerField()

    situacao_tributaria_nfce = models.PositiveIntegerField()

    situacao_tributaria_pis = models.PositiveIntegerField()

    # situacao_tributaria_icms = models.ForeignKey(SituacaoTribIcms, on_delete=models.CASCADE,
    #                                              related_name='situacaotributariaicms')
    #
    # situacao_tributaria_nfce = models.ForeignKey(SituacaoTribIcms, on_delete=models.CASCADE,
    #                                              related_name='situacaotributarianfce')
    #
    # situacao_tributaria_pis = models.ForeignKey(SituacaoTribPis, on_delete=models.CASCADE)

    perc_pis = models.DecimalField("Percentual do PIS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                   help_text='Percentual do pis total a recolher.')

    # TODO Resolver depois
    # situacao_tributaria_cofins = models.ForeignKey(SituacaoTribCofins, on_delete=models.CASCADE)
    situacao_tributaria_cofins = models.IntegerField()

    perc_cofins = models.DecimalField("Percentual do COFINS", max_length=10, max_digits=10, decimal_places=6,
                                      default=0.00, help_text='Percentual do cofins a recolher.')

    # Modalidade  de  determinação da BC da pauta fiscal 0 – Valor mínimo 1 - Valor fixo de pauta independente da venda
    modalidade_pauta_fiscal = models.CharField("Modalidade de cálculo da pauta fiscal?", max_length=1, null=False,
                                               default="3", choices=MODALIDADE_PAUTA_CHOICES,
                                               help_text='Modalidade de cálculo da pauta fiscal')

    pauta_fiscal = models.DecimalField("Valor unitário  para pauta fiscal", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='Valor unitário  para pauta fiscal')

    # 3 valor da operação/0 Margem Valor Agregado(%)/1 Pauta (Valor)/2 Preço Tabelado Máx.(vlr)
    # Modalidade de determinação da BC do ICMS CF NF ELETRÔNICA
    modalidade_calculo_icms = models.CharField("Modalidade de cálculo da base Icms?", max_length=1, null=False,
                                               default="3", choices=MODALIDADE_CALC_ICMS_CHOICES,
                                               help_text='Modalidade de cálculo da base Icms')

    # TODO Resolver depois
    # situacao_tributaria_ipi = models.ForeignKey(SituacaoTribIpi, on_delete=models.CASCADE)
    situacao_tributaria_ipi = models.IntegerField()

    perc_ipi = models.DecimalField("Percentual do IPI a recolher", max_length=10, max_digits=10, decimal_places=6,
                                   default=0.00, help_text='Percentual do IPI a recolher.')

    # percentual de II IMPOSTO   SOBRE importação
    perc_importacao = models.DecimalField("Percentual do II imposto sobre importação", max_length=10, max_digits=10,
                                          decimal_places=6, default=0.00,
                                          help_text='Percentual do II imposto sobre importação')

    perc_importacao_ipi = models.DecimalField("Percentual do II imposto sobre importação IPI", max_length=10,
                                              max_digits=10, decimal_places=6, default=0.00,
                                              help_text='Percentual do II imposto sobre importação IPI')

    perc_desoneracao_icms = models.DecimalField("Percentual de desoneração do icms", max_length=10, max_digits=10,
                                                decimal_places=6, default=0.00,
                                                help_text='Percentual de desoneração do icms')

    motivo_desoneracao_icms = models.CharField("Motivo da desoneração do icms?", max_length=1, null=False,  default="3",
                                               choices=MOTIVO_DESONERACAO_ICM_CHOICES,
                                               help_text='Motivo da desoneração do icms')

    # % imposto de combate a pobreza da Uf destino
    perc_imposto_pobreza_uf_destino = models.DecimalField("% imposto de combate a pobreza da Uf destino", max_length=10,
                                                          max_digits=10, decimal_places=6, default=0.00,
                                                          help_text='% imposto de combate a pobreza da Uf destino')

    perc_icms_pobreza_uf_destino = models.DecimalField("% de icms da Uf destino", max_length=10, max_digits=10,
                                                       decimal_places=6, default=0.00,
                                                       help_text='% icms da Uf destino')

    # % ICMSInterPart-01 provisório de partilha do ICMS Interestadual para a UF de destino: - 40% em 2016; -
    # 60% em 2017; - 80% em 2018; - 100% a partir de
    perc_icms_partilha = models.DecimalField("% de icms de partilha provisório", max_length=10, max_digits=10,
                                             decimal_places=6, default=0.00,
                                             help_text='% de icms de partilha provisório')

    perc_icms_operacao_propria = models.DecimalField("% de icms de operação própria  ", max_length=10, max_digits=10,
                                                     decimal_places=6, default=0.00,
                                                     help_text='% de icms de operação própria')
    ultima_alteracao = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.produto) + "-" + str(self.estado) + "-" + str(self.tipooperacaofiscal)

    class Meta:
        unique_together = ('produto', 'estado', 'tipooperacaofiscal')
        verbose_name = 'Produto Tributação'
        verbose_name_plural = 'Produtos Tributações'


# ----------------------------------------------------------------------------------------------------------------------
# Cadastro de codigos adicionais referenciados do produto
# antigo kcei01g
# ----------------------------------------------------------------------------------------------------------------------
class ProdutoCodigo(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)

    descricao = models.CharField("Descrição do Código adicional", max_length=60, null=False, default=" ",
                                 help_text='Descrição do Código adicional do produto para venda ou produção')

    codigo_adicional = models.CharField("Descrição do Código adicional", max_length=25, null=False, default=" ",
                                        help_text='Descrição do Código adicional do produto para venda ou produção')

    # 0-Grin 1-Alternativo 2-Referência de fábrica 3-anterior ou alternativo
    tipo_codigo = models.CharField("Tipo de Código gravado?", max_length=1, null=False,  default="3",
                                   choices=TIPO_CODIGO_CHOICES,
                                   help_text='Tipo de Código gravado')

    # cor deste produto na grade
    codigo_cor = models.ForeignKey(ProdutoCor, on_delete=models.CASCADE)

    # tamanho
    codigo_tamanho = models.ForeignKey(ProdutoTamanho, on_delete=models.CASCADE)

    codigo_densidade = models.ForeignKey(ProdutoDensidade, on_delete=models.CASCADE)

    preco_venda = models.DecimalField("Preço de venda diferenciado", max_length=16, max_digits=16, decimal_places=2,
                                      default=0.00, help_text='Preço de venda diferenciado')

    embalagem_produto = models.CharField("Embalagem de venda", max_length=15, null=False, default="N",
                                         help_text='Embalagem de venda diferenciada da unidade de venda. '
                                                   'Pode-se vender UNI e embalar em caixa')

    quantidade_por_embalagem = models.DecimalField("Quantidade por embalagem", max_length=16, max_digits=16,
                                                   decimal_places=6, default=1.00,
                                                   help_text='Quantidade por embalagem de compra para efeito de '
                                                             'conversão na hora da entrada da NFe')

    multiplica_divide = models.CharField("Multiplica ou divide na NF entrada", max_length=1, null=False, default="X",
                                         choices=MULTIPLICA_DIVIDE_CHOICES,
                                         help_text='X para multiplicar a quantidade de entrada pela quantidade  por '
                                                   'embalagem e / para dividir na entrada')


# -----------------------------------------------------------------------------------------------------------------------
# Cadastro de codigos adicionais referenciados do produto
# -----------------------------------------------------------------------------------------------------------------------
class ProdutoEstatisticas(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)

    # Média de vendas dos últimos
    media_vendas = models.DecimalField("Média de vendas últimos meses configurados", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='Média de vendas últimos meses configurados conforme configuração abc')

    # quantidade de itens reservados para clientes - verificado durante a venda
    reservado = models.DecimalField("Média de vendas últimos meses configurados", max_length=16, max_digits=16,
                                    decimal_places=6, default=0.00,
                                    help_text='Média de vendas últimos meses configurados conforme configuração abc')

    minimo = models.DecimalField("Mínimo em estoques", max_length=16, max_digits=16, decimal_places=6, default=0.00)
    maximo = models.DecimalField("Máximo em estoques", max_length=16, max_digits=16, decimal_places=6, default=0.00)

    ponto_ressuprimento = models.DecimalField("Ponto de ressuprimento", max_length=16, max_digits=16,
                                              decimal_places=6, default=0.00,)

    pontos_fidelizacao = models.DecimalField("Número de pontos para fidelização", max_length=16, max_digits=16,
                                             decimal_places=6, default=0.00,
                                             help_text='Quantidade de pontos que vale este produto no modulo de '
                                                       'fidelização de clientes  Se zeros sistema assume 1$=1Pto')

    # Este campo somente deve ser preenchido quando cliente não utiliza módulo de compras que é de onde vem o prazo
    # para reposição
    # prazo reposição=Data chegada produto - Data do Pedido em dias
    prazo_reposicao = models.PositiveIntegerField("Prazo de reposição deste produto", null=False,
                                                  validators=[MaxValueValidator(9999)],
                                                  help_text='Prazo de reposição deste produto, Número de dias fixado '
                                                            'para sistema considerar como prazo de reposição')

    # classificação abc será calculada mensalmente no fechamento mensal automático ou nos primeiros minutos do dia
    # primeiro de cada mes
    classe_abc_demanda = models.CharField("Classe Abc Demanda", max_length=1, null=False, default="F")
    classe_abc_financeiro = models.CharField("Classe Abc financeiro", max_length=1, null=False, default="F")
    classe_abc_popularidade = models.CharField("Classe Abc popularidade", max_length=1, null=False, default="F")
    classe_abc_rentabilidade = models.CharField("Classe Abc rentabilidade", max_length=1, null=False, default="F")
    classe_abc_frequencia = models.CharField("Classe Abc frequência de vendas", max_length=1, null=False, default="F")


# ----------------------------------------------------------------------------------------------------------------------
# PEDIDOS DE VENDAS ORÇAMENTOS ENCOMENDAS REQUISIÇÕES ETC (KCEI03)
# ----------------------------------------------------------------------------------------------------------------------
class Pedido(models.Model):
    # id do será o Número do pedido
    # Série será as 3 primeiras letras do Código da empresa
    # subserie conforme operação "VEN" "ORC" "ETC"
    serie = models.CharField("Série", max_length=3, null=False, default='MAT')
    subserie = models.CharField("Subsérie", max_length=3, null=False, default='VEN')

    # informação deve ser trazida da tabela TipoDocumento
    indicador_pagamento_nfe = models.CharField("Indicador da forma de pagamento", max_length=1, null=False, default="0",
                                               choices=INDICADOR_PAGAMENTO_CHOICES,
                                               help_text='Indicador da forma de pagamento para informação na nota '
                                                         'fiscal eletrônica')

    # Orçamento/Devolução/Cancelado/Em análise crédito/Bloqueado/Faturado/quitado Aprovado para faturamento
    status_pedido = models.CharField("Status deste pedido", max_length=1, null=False, default="A",
                                     choices=STATUS_PEDIDO_ITEM_CHOICES,
                                     help_text='status do pedido Orçamento/Devolução/Cancelado/Em análise crédito/'
                                               'Bloqueado/Faturado/quitado etc ')

    # Código do regime Tributário do emitente ou do fornecedor 1-Simples na 2-Simples exc  3-Normal
    regime_tributario = models.CharField("Regime Tributário Emitente", max_length=1, null=False, default="1",
                                         choices=REGIME_TRIBUTARIO_CHOICES,
                                         help_text='Código do regime Tributário do emitente ou do fornecedor '
                                                   '1-Simples na 2-Simples exc  3-Normal')

    notafiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE,
                                   help_text='Número da nota fiscal emitida para este pedido conforme Número no '
                                             'faturamento da NFe ou NFce')

    # Número da autorização para Faturamento
    autorizacao_faturamento = models.CharField("Número da autorização para Faturamento", max_length=20, null=False,
                                               help_text='Número da autorização de faturamento emitida pelo cliente ou '
                                                         'pelo fornecedor')

    autorizacao_numitem = models.PositiveIntegerField("Número do Pedido", null=True, default=0,
                                                      validators=[MaxValueValidator(99999)],
                                                      help_text='Informe Número do item autorizado a fatura na Af do '
                                                                'fornecedor')

    # Indicador de emitente do documento fiscal
    indicador_emitente = models.CharField("Indicador de emitente da NFe", max_length=1, null=True,
                                          choices=EMISSAO_CHOICES, default="1",
                                          help_text='Indicador de emitente do documento fiscal  0_Emissão própria '
                                                    '1_Terceiros')

    # 00|Doc regular| 01|Doc reg extemporâneo| 02|Doc cancelado|  03|Doc canc extemporâneo| 04|NFe denegada|
    # 05|NFe Numeração inutilizada| 06|Doc Fiscal Compl| 07|Doc Fiscal Compl extemporâneo| 08|Doc RegEspecial
    # Situação da nota fiscal quanto ao cancelamento (item 4.1.2- Tabela Situação do Documento do AtoCOTEPE/ICMS nº 09,
    #  de 2008),
    situacaodocumentosped = models.ForeignKey(SituacaoDocumentoSped,
                                              on_delete=models.CASCADE, null=False, default=1,
                                              help_text='Situação Do Documento Fiscal conforme tabela 4.1.2 do Sped')

    # TODO  Depois tem que mudar para 55
    modelodocumentofiscal = models.ForeignKey(ModeloDocumentoFiscal,
                                              on_delete=models.CASCADE, default=1, null=True, blank=True,
                                              help_text='Código Do Documento Fiscal conforme tabela Sped - '
                                                        'Ex. 55|Nota Fiscal Eletrônica')

    data_pedido = models.DateField('Data de De Emissão da Nfe', null=False, blank=False, auto_now_add=True)
    data_emissao = models.DateField('Data de De Emissão da Nfe', null=False, blank=False, auto_now_add=True)
    data_saida = models.DateTimeField('Data de saida para entrega', null=False, blank=False, auto_now_add=True)
    data_movimento = models.DateTimeField('Data de Movimentação da Nfe', null=False, blank=False, auto_now_add=True)

    # natureza da operação fiscal de base  ou cfop principal que indicará o tipo de saida (nos itens tem vários)
    cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE,
                             help_text='Informe o Cfop - Código fiscal de Operação')

    # tipo de pagamento utilizado neste pedido
    tipo_de_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.CASCADE, related_name='tipopagamento',
                                          default=1, help_text='Informe Código do tipo de pagamento')

    # Prazos para pagamento
    prazo_de_pagamento = models.ForeignKey(PrazoPagamento, on_delete=models.CASCADE,
                                           help_text='Informe Prazos para pagamento')

    # Código do participante (Cliente ou fornecedor) nesta operação fiscal
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='clientes',
                                     help_text='Código do participante (Cliente ou fornecedor) nesta operação fiscal')

    # vendedor responsável pela venda ou comprador
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 help_text='Código do vendedor')

    # mensagem padrao a ser impressa durante a emissão da nota fiscal como observações adicionais na NF
    mensagempadrao = models.ForeignKey(MensagemPadrao, on_delete=models.CASCADE, null=True,
                                       help_text='mensagem padrão a ser impressa durante a emissão da nota fiscal '
                                                 'como observações adicionais na NF')

    # Tipo de movimentação de entrada ou saida
    tipo_pedido = models.ForeignKey(PedidoTipo, on_delete=models.CASCADE, default="00",
                                    help_text='Informe Tipo de movimentação de entrada ou saida')

    # indPres (nfe 3.10) Indicador de presença do comprador no estabelecimento ----
    indicador_presenca_nfe = models.CharField("Indicador de presença do comprador NFe", max_length=1, null=False,
                                              choices=INDICA_PRESENCA_CHOICES, default="1",
                                              help_text='indPres (nfe 3.10) Indicador de presença do comprador no '
                                                        'estabelecimento comercial no momento da operação')

    # Tipo de Preço usado na saida de pedidos da tabela
    tipo_preco_pedido = models.CharField(max_length=1, null=False, default="V",
                                         help_text='Tipo de Preço usado na saida de pedidos V Preço VENDA / '
                                                   'C Último CUSTO / I Preço indexado, etc')

    # Total bruto (sem descontos) dos  produtos no pedido
    total_produtos = models.DecimalField("Total dos Produtos", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00,
                                         help_text='Total bruto (sem descontos) dos produtos no pedido')
    # Percentual  % desconto total na Nf para rateio por item nos itens
    perc_desc = models.DecimalField("Percentual de descontos nos produtos", max_length=10, max_digits=10,
                                    decimal_places=6, default=0.00,
                                    help_text='Percentual de descontos nos produtos')
    # valor do desconto na nota fiscal em totais (valor dos descontos em % + valor dos descontos em valores do pedido)
    descont_valor = models.DecimalField("Valor desconto no Pedido", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00,
                                        help_text='valor do desconto na nota fiscal em totais (valor dos descontos em %'
                                                  ' + valor dos descontos em valores do pedido')

    # valores de cálculo do IPI
    base_calc_ipi = models.DecimalField("Base de cálculo do IPI", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Base de cálculo do IPI')
    valor_ipi = models.DecimalField("Valor do IPI", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                    help_text='Valor calculado do IPI a recolher.')
    perc_ipi = models.DecimalField("Percentual do IPI", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                   help_text='Percentual do IPI a recolher.')

    # Total líquido do pedido (somatório dos produtos - descontos + impostos + frete + outros valores)
    valor_contabil = models.DecimalField("Total Líquido do Pedido", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00,
                                         help_text='Total líquido do pedido/total líquido da Nota fiscal pedido.')

    base_calc_icms = models.DecimalField("Base de cálculo do ICMS", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00,
                                         help_text='Base de cálculo do ICMS.')
    valor_icms = models.DecimalField("Valor do ICMS", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                     help_text='Valor calculado do ICMS a recolher.')
    perc_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                    help_text='Percentual do ICMS a recolher.')

    # valores de cálculo do ICMS substituição tributária
    # valor do icms a calculado=valor_icms_sub - valor_icms
    base_calc_icms_sub = models.DecimalField("Base de cálculo do Icms Substituição", max_length=16,
                                             max_digits=16, decimal_places=2, default=0.00,
                                             help_text='Base de cálculo do Icms Substituição tributária')
    valor_icms_sub = models.DecimalField("Valor do ICMS substituição tributária", max_length=16,
                                         max_digits=16, decimal_places=2, default=0.00,
                                         help_text='Valor do ICMS substituição tributária')

    # valor das despesas acessórias para rateio por item
    valor_despesas_acess = models.DecimalField("Valor despesas acessorias", max_length=16, max_digits=16,
                                               decimal_places=2, default=0.00,
                                               help_text='Valor das despesas acessórias')

    # valor do pis para rateio por item
    base_calc_pis = models.DecimalField("Valor Base de cálculo do Pis", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Valor Base de cálculo do PIS')

    valor_pis = models.DecimalField("Valor do Pis", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                    help_text='Valor do pis')

    # valor do cofins para rateio por item
    base_calc_cofins = models.DecimalField("Valor Base de cálculo do cofins", max_length=16, max_digits=16,
                                           decimal_places=2, default=0.00,
                                           help_text='Valor Base de cálculo do cofins')
    valor_cofins = models.DecimalField("Valor do cofins", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                       help_text='Valor do cofins')

    # valor do seguro
    valor_seguro = models.DecimalField("Valor do cofins", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                       help_text='Valor do cofins')

    # valor dos serviços se nfe for de serviços
    base_calc_issqn = models.DecimalField("Base de cálculo serviços", max_length=16,
                                          max_digits=16, decimal_places=2, default=0.00,
                                          help_text='valor Base de cálculo serviços se nfe for de serviços')
    perc_issqn = models.DecimalField("Percentual do ISS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                     help_text='Percentual do ISS a recolher.')
    quantidade_servicos = models.DecimalField("Quantidade de serviços", max_length=10,
                                              max_digits=10, decimal_places=6, default=0.00,
                                              help_text='Quantidade dos serviços se nfe for de serviços')
    valor_servicos = models.DecimalField("Valor dos serviços", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00,
                                         help_text='valor dos serviços se nfe for de serviços')

    # valor do frete neste operação fiscal e Código da transportadora
    transportadora = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='transportadoras',
                                       help_text='Código da transportadora nesta operação fiscal')
    valor_frete = models.DecimalField("Valor do FRETE", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                      help_text='Valor do frete na nota fiscal de entrada ou de saida')
    valor_icm_frete = models.DecimalField("Valor do icms sobre o frete", max_length=16, max_digits=16,
                                          decimal_places=2, default=0.00,
                                          help_text='Valor do icms sobre o frete na nota fiscal de entrada ou de saida')
    cif_fob_frete = models.CharField("Indicador do tipo de frete", max_length=1, null=False,  default="1",
                                     choices=INDICADOR_FRETE_CHOICES,
                                     help_text='Indicador de frete. 0-Emitente, 1-Destinatário, 2-Terceiros, '
                                               '3-Próprio remetente, 4-Próprio destinatário, 9-Sem')
    tipo_frete = models.CharField("Indicador do custo do frete", max_length=1, null=False, default="1",
                                  choices=TIPO_FRETE_CHOICES,
                                  help_text='1 Frete na NFe COM cre 2-Incluso na Nfe sem credito 3-Conhec a parte '
                                            '4-Conhec parte sem cred')

    status_manifestacao = models.CharField(max_length=1, null=False, default="C",
                                           choices=STATUS_CONFERENCIA_CHOICES,
                                           help_text='Status de conferência na manifestação de destinatário para efeito'
                                                     ' de liberação de produtos para venda')

    status_contabilidade = models.CharField(max_length=1, null=False, default="C",
                                            choices=STATUS_CONFERENCIA_CHOICES,
                                            help_text='Status de conferência da NF  pela contabilidade informando que'
                                                      ' nf está fiscalmente OK')

    status_financeiro = models.CharField(max_length=1, null=False, default="A",
                                         choices=STATUS_CONFERENCIA_CHOICES,
                                         help_text='Status de conferência da NF  pelo departamento financeiro '
                                                   'informando que nf está financeiramente (contas a pagar) OK')

    status_precos = models.CharField(max_length=1, null=False, default="C",
                                     choices=STATUS_CONFERENCIA_CHOICES,
                                     help_text='Status de conferência da NF  pelo departamento custos informando que '
                                               'nf está com preços e custos OK')

    status_expedicao = models.CharField(max_length=1, null=False, default="L", choices=STATUS_CONFERENCIA_CHOICES,
                                        help_text='Status de conferência da NF  pela expedição informando que nf está '
                                                  'com quantidades armazenadas OK')

    # "S" para que nf esteja totalizada OK  E SEM DIFERENÇA
    # "D" para NF com diferença e com saldo não atualizado

    status_diferenca = models.CharField(max_length=1, null=False, default="C", choices=STATUS_DIFERENCA_CHOICES,
                                        help_text='Status de conferencia dos valores na nota fiscal de entrada ou '
                                                  'saida para ver se há diferenças')
    ultima_alteracao = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.serie) + ' ' + str(self.subserie)

    class Meta:
        verbose_name = 'Cadastro de Pedido'
        verbose_name_plural = 'Cadastro de Pedidos'
        # index_together = [
        #     ['participante', 'data_movimento'],
        #     ['data_movimento', 'notafiscal'],
        #     ['notafiscal', 'participante']
        # ]


# ------------------------------------------------------------------------------------------------------------------
# itens do pedido
# ------------------------------------------------------------------------------------------------------------------
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    sequencia = models.PositiveIntegerField("Sequência do item", null=False, default=1,
                                            help_text='Informe valor numerico e maior que zeros para Número de item do '
                                                      'pedido 001 a 999 itens por nota fiscal')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    unidade = models.CharField(max_length=13, null=False, default=" ",
                               help_text='Unidade do produto vendido conforme cadastro no momento da venda. A mesma do'
                                         ' cadastro de produtos')

    descricao = models.CharField(max_length=60, null=False, default=" ",
                                 help_text='Descrição do produto vendido conforme cadastro no momento da venda. A mesma'
                                           ' do cadastro de produtos')

    observacoes = models.CharField(max_length=40, null=False, default=" ",
                                   help_text='Observação para efeito de informação fiscal especifica neste produto')

    # natureza da operação fiscal de base  ou cfop que indicará o tipo de operação
    # (cfop+data) (data+cfop)
    cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE,
                             help_text='natureza de operação fiscal específica deste produto')

    codigo_ncm = models.ForeignKey(CodigoNcm, on_delete=models.CASCADE)

    codigo_cest = models.ForeignKey(CodigoCest, on_delete=models.CASCADE)

    # Orçamento/Devolução/Cancelado/Em análise crédito/Bloqueado/Faturado/quitado etc
    status_pedido_item = models.CharField("Status deste pedido", max_length=1, null=False, default="N",
                                          choices=STATUS_PEDIDO_ITEM_CHOICES,
                                          help_text='status do pedido Orçamento/Devolução/Cancelado/Em análise '
                                                    'crédito/Bloqueado/Faturado/quitado etc ')

    # Número da autorização para Faturamento
    autorizacao_faturamento = models.CharField("Número da autorização para Faturamento", max_length=20, null=False,
                                               help_text='Número da autorização de faturamento emitida pelo cliente '
                                                         'ou pelo fornecedor')
    autorizacao_numitem = models.PositiveIntegerField("Número do Pedido", null=False,
                                                      validators=[MaxValueValidator(99999)],
                                                      help_text='Informe Número do item autorizado a fatura na Af do '
                                                                'fornecedor')

    quantidade = models.DecimalField("Quantidade vendida de produtos", max_length=16, max_digits=16, decimal_places=6,
                                     default=0.00, validators=[quantidade_maior_que_zero],
                                     help_text='Quantidade vendida de produtos no pedido e nota fiscal de entrada ou '
                                               'de saida')

    peso_liquido = models.DecimalField("Peso líquido do produto", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='peso líquido deste produto ')
    peso_bruto = models.DecimalField("Peso bruto do produto", max_length=16, max_digits=16,
                                     decimal_places=6, default=0.00,
                                     help_text='peso bruto deste produto ')

    metro_cubico = models.DecimalField("metros cúbicos do produto", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='metros cúbicos do produto')

    # movimenta estoques - campo trazido do cadastro de CFOP mas que pode ser alterado
    # campo com "N" sempre que a n nota fiscal estiver bloqueada para análise
    movimenta_estoques = models.CharField("Movimenta Estoques?", max_length=1, null=False,  default="N",
                                          choices=SIM_NAO_CHOICES,
                                          help_text='S para movimentar estoques e N para não movimentar')

    saldo_fisico = models.DecimalField("Saldo físico do produto após gravação do pedido", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='Saldo físico do produto após gravação')

    saldo_fiscal = models.DecimalField("Saldo físico do produto após gravação", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='Saldo fiscal do produto após geração e gravação  da nota fiscal '
                                                 'emitida ou recebida')

    preco_custo = models.DecimalField("Preço de custo calculado após gravação", max_length=16, max_digits=16,
                                      decimal_places=6, default=0.00,
                                      help_text='Preço de custo do produto após gravada da nota fiscal de entrada '
                                                'ou saida')
    preco_medio = models.DecimalField("Preço de custo médio calculado após gravação", max_length=16, max_digits=16,
                                      decimal_places=6, default=0.00,
                                      help_text='Preço de custo médio do produto após gravada da nota fiscal de '
                                                'entrada ou saida')
    preco_custo_nfe = models.DecimalField("Preço de custo calculado após gravação da NFe", max_length=16, max_digits=16,
                                          decimal_places=6, default=0.00,
                                          help_text='Preço de custo do produto após gravada da nota fiscal de entrada '
                                                    'ou saida')
    preco_medio_nfe = models.DecimalField("Preço de custo médio calculado após gravação da Nfe", max_length=16,
                                          max_digits=16, decimal_places=6, default=0.00,
                                          help_text='Preço de custo médio do produto após gravada a nota fiscal de '
                                                    'entrada ou saida')

    preco_unitario = models.DecimalField("Preço unitário  de venda", max_length=16, max_digits=16, decimal_places=6,
                                         default=0.00,
                                         help_text='Preço unitário  de venda conforme negociação e configurações '
                                                   'do sistema')
    perc_desc = models.DecimalField("Percentual de descontos no produto", max_length=10, max_digits=10,
                                    decimal_places=6, default=0.00,
                                    help_text='Percentual de descontos nos produtos')

    custo_informado = models.DecimalField("Preço gerencial de venda", max_length=16, max_digits=16,
                                          decimal_places=6, default=0.00,
                                          help_text='Preço gerencial de venda conforme negociação para efeito de '
                                                    'cálculo de Preço de venda')

    # data de movimento lembrar (codigo + data) e (data+codigo) servirão para diversas operações no sistema
    data_movimento = models.DateTimeField('Data de Movimentação do produto', null=False, blank=False,
                                          help_text='Data de Movimentação do produto. Mesma data do pedido para efeito '
                                                    'de cálculo de saldos (Codigo+data)')
    # Código do participante (Cliente ou fornecedor) nesta operação fiscal -
    # participante+data) (data+participante) (participante+codigo) (codigo+participante)- relatorios extratos
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='fornecedores',
                                     help_text='Código do participante (Cliente ou fornecedor) nesta operação fiscal')

    # Total bruto (sem descontos) dos  produtos no pedido
    total_produto = models.DecimalField("Total do Produto", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Total bruto (sem descontos) do produto no pedido')

    # valores de cálculo do IPI  - indicação de tributação  de IPI 1=trib 2=Isento ou não trib 3=
    modalidade_ipi = models.CharField("Modalidade de cálculo do IPI ?", max_length=1, null=False,  default="3",
                                      choices=MODALIDADE_IPI_CHOICES,
                                      help_text='Modalidade de cálculo da base Icms')
    situacao_tributaria_ipi = models.ForeignKey(SituacaoTribIpi, on_delete=models.CASCADE,
                                                null=False, help_text='Código da situação tributária quanto ao pis '
                                                                      'nesta operação fiscal')
    base_calc_ipi = models.DecimalField("Base de cálculo do IPI", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Base de cálculo do IPI=valor produtos - descontos')
    perc_ipi = models.DecimalField("Percentual do IPI", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                   help_text='Percentual do IPI a recolher.')
    perc_red_ipi = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                       decimal_places=6, default=0.00,
                                       help_text='Percentual de redução de base do IPI.')

    # 3 valor da operação/0 Margem Valor Agregado(%)/1 Pauta (Valor)/2 Preço Tabelado Máx.(vlr)
    modalidade_calculo = models.CharField("Modalidade de cálculo da base Icms?", max_length=1, null=False,  default="3",
                                          choices=MODALIDADE_CALC_ICMS_CHOICES,
                                          help_text='Modalidade de cálculo da base Icms')
    # indicação de tributação  de ICMS 1=trib 2=Isento ou não trib 3=
    modalidade_icms = models.CharField("Modalidade de cálculo da base Icms?", max_length=1, null=False,  default="3",
                                       choices=MODALIDADE_ICMS_CHOICES,
                                       help_text='Modalidade de cálculo da base Icms')
    situacao_tributaria_icms = models.ForeignKey(SituacaoTribIcms, on_delete=models.CASCADE,
                                                 null=False, help_text='Código da situação tributária quanto ao Icms '
                                                                       'nesta operação fiscal')
    base_calc_icms = models.DecimalField("Base de cálculo do ICMS", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Base de cálculo do ICMS.')
    perc_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                    help_text='Percentual redução de base cálculo Icms.')
    perc_antec_tributaria = models.DecimalField("Percentual de antecipação tributária do ICMS", max_length=10,
                                                max_digits=10, decimal_places=6, default=0.00,
                                                help_text='Percentual de antecipação tributária do ICMS para efeito de '
                                                          'cálculo do custo de entrada')
    perc_red_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6,
                                        default=0.00, help_text='Percentual redução de base calc Icms.')

    base_calc_icms_sub = models.DecimalField("Base de cálculo do Icms Substituição", max_length=16,
                                             max_digits=16, decimal_places=2, default=0.00)
    perc_mva_sub = models.DecimalField("Percentual do MVA", max_length=10, max_digits=10, decimal_places=6,
                                       default=0.00, help_text='MVA para efeito de cálculo da base de icms substituição'
                                                               ' tributária')
    perc_icms_sub = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6,
                                        default=0.00, help_text='Percentual redução de base cálculo Icms.')
    perc_reducao_icms_sub = models.DecimalField("Percentual de reducao do ICMS Sub", max_length=10, max_digits=10,
                                                decimal_places=6, default=0.00,
                                                help_text='Percentual redução de base calc Icms substituição '
                                                          'tributária.')

    base_calc_antecipacao_trib = models.DecimalField("Base de cálculo da antecipação tributária se houver.",
                                                     max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                                     help_text='Base de cálculo da antecipação tributária se houver.')
    perc_antecipacao_trib = models.DecimalField("% para cálculo da antecipação tributária se houver.", max_length=10,
                                                max_digits=10, decimal_places=6, default=0.00,
                                                help_text='% para cálculo da antecipação tributária se houver.')

    situacao_tributaria_pis = models.ForeignKey(SituacaoTribPis, on_delete=models.CASCADE,
                                                null=False, help_text='Código da situação tributária quanto ao pis '
                                                                      'nesta operação fiscal')
    base_calc_pis = models.DecimalField("Valor Base de cálculo do Pis", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Valor Base de cálculo do Pis')
    perc_pis = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                   decimal_places=6, default=0.00, help_text='Percentual de redução de base do IPI.')

    # Código da Base de Cálculo do Crédito apurado no período, conforme a Tabela 4.3.7. SPED PIS COFINS
    # TODo natureza_base_pis = models.ForeignKey(NaturezaBasePis, on_delete=models.CASCADE)
    # tabela 4.3.6 - Tabela Código de Tipo de Crédito - Atualizada em 03/01/2012 : REGISTRO M500: CRÉDITO DE COFINS
    # RELATIVO AO PERÍODO
    # TODO tipo_credito_base_pis = models.ForeignKey(CódigoTipoCreditoPis, on_delete=models.CASCADE)

    situacao_tributaria_cofins = models.ForeignKey(SituacaoTribCofins, on_delete=models.CASCADE,
                                                   null=False, help_text='Código da situação tributária quanto ao '
                                                                         'Cofins nesta operação fiscal')
    base_calc_cofins = models.DecimalField("Valor Base de cálculo do cofins", max_length=16, max_digits=16,
                                           decimal_places=2, default=0.00, help_text='Valor Base de cálculo do cofins')

    perc_fundo_pobreza = models.DecimalField("Percentual para fundo de combate a pobreza", max_length=10, max_digits=10,
                                             decimal_places=6, default=0.00, help_text='Percentual para fundo de '
                                                                                       'combate a pobreza')
    # LEI DA TRANSPARÊNCIA FISCAL NOTA TÉCNICA 003 2013 % DE TRIBUTOS TOTAL NESTE ITEM
    perc_trib_aproximado = models.DecimalField("Percentual aprox trib lei transp fiscal", max_length=10, max_digits=10,
                                               decimal_places=6, default=0.00,
                                               help_text='Percentual aproximado de tributação conforme lei '
                                                         'transparência fiscal')

    base_calc_import = models.DecimalField("Valor Base de cálculo do imposto sobre importação", max_length=16,
                                           max_digits=16, decimal_places=2, default=0.00,
                                           help_text='Valor Base de cálculo do imposto sobre importação')
    perc_import = models.DecimalField("Percentual de II imposto sobre importação", max_length=10, max_digits=10,
                                      decimal_places=6, default=0.00,
                                      help_text='Percentual de II imposto sobre importação')

    # valor dos serviços se nfe for de serviços
    base_calc_issqn = models.DecimalField("Base de cálculo serviços", max_length=16, max_digits=16, decimal_places=2,
                                          default=0.00,
                                          help_text='valor Base de cálculo serviços se nfe for de serviços')
    perc_issqn = models.DecimalField("Percentual do ISS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                     help_text='Percentual do ISS a recolher.')

    # % das despesas acessórias para rateio por item
    perc_desp_acessorias = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                               decimal_places=6, default=0.00,
                                               help_text='Percentual de redução de base do IPI.')
    perc_seguro = models.DecimalField("Percentual de seguro neste Produto", max_length=10, max_digits=10,
                                      decimal_places=6, default=0.00, help_text='Percentual de seguro ')
    perc_frete = models.DecimalField("Percentual de frete neste Produto", max_length=10, max_digits=10,
                                     decimal_places=6, default=0.00, help_text='Percentual de frete ')

    # Natureza de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    natureza_custos = models.ForeignKey(NaturezaCusto, default=1, on_delete=models.CASCADE,
                                        help_text='Natureza de custos deste tipo de operação de venda ou para qual '
                                                  'conta de custos sistema irá')

    # Centro de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    centro_custos = models.ForeignKey(CentroCusto, default=1, on_delete=models.CASCADE,
                                      help_text='Centro de custos deste tipo de operação de venda ou para qual conta de'
                                                ' custos sistema irá')

    # Código da promoção no cadastro de produtos corrente quando foi feita esta venda
    codigo_promocao = models.ForeignKey(ProdutoPromocao, default=0, on_delete=models.CASCADE,
                                        help_text='Código da promoção desta venda na hora da venda')
    ultima_alteracao = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.pedido) + ' ' + str(self.item) + ' ' + str(self.produto)

    class Meta:
        unique_together = ("pedido", "sequencia", "produto")
        verbose_name = 'Cadastro de Pedido'
        verbose_name_plural = 'Cadastro de Pedidos'


# ----------------------------------------------------------------------------------------------------------------------
# PEDIDOS DE VENDAS ORÇAMENTOS ENCOMENDAS REQUISIÇÕES ETC (KCEI03)
# ----------------------------------------------------------------------------------------------------------------------
class PedidoNf(models.Model):
    # id do será o Número do pedido
    # Série será as 3 primeiras letras do Código da empresa
    # subsérie conforme operação "VEN" "ORC" "ETC"
    serie = models.CharField("Série", max_length=3, null=False, default='MAT')
    subserie = models.CharField("Subsérie", max_length=3, null=False, default='VEN')

    # informação deve ser trazida da tabela TipoDocumento
    indicador_pagamento_nfe = models.CharField("Indicador da forma de pagamento", max_length=1, null=False, default="0",
                                               choices=INDICADOR_PAGAMENTO_CHOICES,
                                               help_text='Indicador da forma de pagamento para informação na nota '
                                                         'fiscal eletrônica')

    # Orçamento / Devolução / Cancelado / Em análise crédito / Bloqueado / Faturado/quitado Aprovado para faturamento
    status_pedido = models.CharField("Status deste pedido", max_length=1, null=False, default="A",
                                     choices=STATUS_PEDIDO_ITEM_CHOICES,
                                     help_text='status do pedido Orçamento/Devolução/Cancelado/Em análise crédito / '
                                               'Bloqueado/Faturado/quitado etc ')

    # Código do regime Tributário do emitente ou do fornecedor 1-Simples na 2-Simples exc  3-Normal
    regime_tributario = models.CharField("Regime Tributário Emitente", max_length=1, null=False, default="1",
                                         choices=REGIME_TRIBUTARIO_CHOICES,
                                         help_text='Código do regime Tributário do emitente ou do fornecedor '
                                                   '1-Simples na 2-Simples exc  3-Normal')

    notafiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE,
                                   help_text='Número da nota fiscal emitida para este pedido conforme Número no '
                                             'faturamento da NFe ou NFce')

    # Número da autorização para Faturamento
    autorizacao_faturamento = models.CharField("Número da autorização para Faturamento", max_length=20, null=False,
                                               help_text='Número da autorização de faturamento emitida pelo cliente '
                                                         'ou pelo fornecedor')

    autorizacao_numitem = models.PositiveIntegerField("Número do Pedido", null=True,
                                                      validators=[MaxValueValidator(99999)],
                                                      help_text='Informe número do item autorizado a fatura na Af do '
                                                                'fornecedor')

    # Indicador de emitente do documento fiscal
    indicador_emitente = models.CharField("Indicador de emitente da NFe", max_length=1, null=True,
                                          choices=EMISSAO_CHOICES, default="1",
                                          help_text='Indicador de emitente do documento fiscal  0_Emissão própria '
                                                    '1_Terceiros')

    # 00|Doc regular| 01|Doc reg extemporâneo| 02|Doc cancelado|  03|Doc canc extemporâneo| 04|NFe denegada|
    # 05|NFe Numeração inutilizada| 06|Doc Fiscal Compl| 07|Doc Fiscal Compl extemporâneo| 08|Doc RegEspecial
    # Situação da nota fiscal quanto ao cancelamento (item 4.1.2- Tabela Situação do Documento do Ato COTEPE/ICMS nº 09,
    # de 2008),
    situacaodocumentosped = models.ForeignKey(SituacaoDocumentoSped, on_delete=models.CASCADE, default=1,
                                              help_text='Situação Do Documento Fiscal conforme tabela 4.1.2 do Sped')

    # TODO  Depois tem que mudar para 55
    modelodocumentofiscal = models.ForeignKey(ModeloDocumentoFiscal,
                                              on_delete=models.CASCADE, default=1,
                                              help_text='Código Do Documento Fiscal conforme tabela Sped - '
                                                        'Ex. 55|Nota Fiscal Eletrônica')

    data_pedido = models.DateField('Data de De Emissão da Nfe', null=False, blank=False, auto_now_add=True)
    data_emissao = models.DateField('Data de De Emissão da Nfe', null=False, blank=False, auto_now_add=True)
    data_saida = models.DateTimeField('Data de saida para entrega', null=False, blank=False, auto_now_add=True)
    data_movimento = models.DateTimeField('Data de Movimentação da Nfe', null=False, blank=False, auto_now_add=True)

    # natureza da operação fiscal de base  ou cfop principal que indicará o tipo de saida (nos itens tem vários)
    cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE, help_text='Informe o Cfop - Código fiscal de Operação')

    # tipo de pagamento utilizado neste pedido
    tipo_de_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.CASCADE, default=1,
                                          related_name='tipopagamentoNF', help_text='Informe código do tipo de pagamento')

    # Prazos para pagamento
    prazo_de_pagamento = models.ForeignKey(PrazoPagamento, on_delete=models.CASCADE,
                                           help_text='Informe Prazos para pagamento')

    # Código do participante (Cliente ou fornecedor) nesta operação fiscal
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='clientesNF',
                                     help_text='Código do participante (Cliente ou fornecedor) nesta operação fiscal')

    # vendedor responsável pela venda ou comprador
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Código do vendedor')

    # mensagem padrão a ser impressa durante a emissão da nota fiscal como observações adicionais na NF
    mensagempadrao = models.ForeignKey(MensagemPadrao, on_delete=models.CASCADE,
                                       help_text='mensagem padrao a ser impressa durante a emissão da nota fiscal '
                                                 'como observações adicionais na NF')

    # Tipo de movimentação de entrada ou saida
    tipo_pedido = models.ForeignKey(PedidoTipo, on_delete=models.CASCADE,
                                    default="00", help_text='Informe Tipo de movimentação de entrada ou saida')

    # indPres (nfe 3.10) Indicador de presença do comprador no estabelecimento ----
    indicador_presenca_nfe = models.CharField("Indicador de presença do comprador NFe", max_length=1, null=False,
                                              choices=INDICA_PRESENCA_CHOICES, default="1",
                                              help_text='indPres (nfe 3.10) Indicador de presença do comprador no '
                                                        'estabelecimento comercial no momento da operação')

    # Tipo de Preço usado na saida de pedidos da tabela
    tipo_preco_pedido = models.CharField(max_length=1, null=False, default="V",
                                         help_text='Tipo de Preço usado na saida de pedidos V Preço VENDA / '
                                                   'C Último CUSTO / I Preço indexado, etc')

    # Total bruto (sem descontos) dos  produtos no pedido
    total_produtos = models.DecimalField("Total dos Produtos", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Total bruto (sem descontos) dos  produtos no '
                                                                 'pedido')
    # Percentual  % desconto total na Nf para rateio por item nos itens
    perc_desc = models.DecimalField("Percentual de descontos nos produtos", max_length=10, max_digits=10,
                                    decimal_places=6, default=0.00, help_text='Percentual de descontos nos produtos')
    # valor do desconto na nota fiscal em totais (valor dos descontos em % + valor dos descontos em valores do pedido)
    desconto_valor = models.DecimalField("Valor desconto no Pedido", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='valor do desconto na nota fiscal em totais (valor '
                                                                 'dos descontos em % + valor dos descontos em valores '
                                                                 'do pedido')

    # valores de cálculo do IPI
    base_calc_ipi = models.DecimalField("Base de cálculo do IPI", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Base de cálculo do IPI')
    valor_ipi = models.DecimalField("Valor do IPI", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                    help_text='Valor calculado do IPI a recolher.')
    perc_ipi = models.DecimalField("Percentual do IPI", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                   help_text='Percentual do IPI a recolher.')

    # Total líquido do pedido (somatório dos produtos - descontos + impostos + frete + outros valores)
    valor_contabil = models.DecimalField("Total Líquido do Pedido", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Total líquido do pedido/total líquido da Nota fiscal '
                                                                 'pedido.')

    base_calc_icms = models.DecimalField("Base de cálculo do ICMS", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Base de cálculo do ICMS.')
    valor_icms = models.DecimalField("Valor do ICMS", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                     help_text='Valor calculado do ICMS a recolher.')
    perc_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                    help_text='Percentual do ICMS a recolher.')

    # valores de cálculo do ICMS substituição tributária
    # valor do icms a calculado=valor_icms_sub - valor_icms
    base_calc_icms_sub = models.DecimalField("Base de cálculo do Icms Substituição", max_length=16,
                                             max_digits=16, decimal_places=2, default=0.00,
                                             help_text='Base de cálculo do Icms Substituição tributária')
    valor_icms_sub = models.DecimalField("Valor do ICMS substituição tributária", max_length=16,
                                         max_digits=16, decimal_places=2, default=0.00,
                                         help_text='Valor do ICMS substituição tributária')

    # valor das despesas acessórias para rateio por item
    valor_despesas_acess = models.DecimalField("Valor despesas acessórias", max_length=16,
                                               max_digits=16, decimal_places=2, default=0.00,
                                               help_text='Valor das despesas acessórias')

    # valor do pis para rateio por item
    base_calc_pis = models.DecimalField("Valor Base de cálculo do Pis", max_length=16,
                                        max_digits=16, decimal_places=2, default=0.00,
                                        help_text='Valor Base de cálculo do Pis')

    valor_pis = models.DecimalField("Valor do Pis", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                    help_text='Valor do pis')

    # valor do cofins para rateio por item
    base_calc_cofins = models.DecimalField("Valor Base de cálculo do cofins", max_length=16,
                                           max_digits=16, decimal_places=2, default=0.00,
                                           help_text='Valor Base de cálculo do cofins')
    valor_cofins = models.DecimalField("Valor do cofins", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                       help_text='Valor do cofins')

    # valor do seguro
    valor_seguro = models.DecimalField("Valor do cofins", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                       help_text='Valor do cofins')

    # valor dos serviços se nfe for de serviços
    base_calc_issqn = models.DecimalField("Base de cálculo serviços", max_length=16, max_digits=16, decimal_places=2,
                                          default=0.00,
                                          help_text='valor Base de cálculo serviços se nfe for de serviços')
    perc_issqn = models.DecimalField("Percentual do ISS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                     help_text='Percentual do ISS a recolher.')
    quantidade_servicos = models.DecimalField("Quantidade de serviços", max_length=10, max_digits=10, decimal_places=6,
                                              default=0.00, help_text='Quantidade dos serviços se nfe for de serviços')
    valor_servicos = models.DecimalField("Valor dos serviços", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='valor dos serviços se nfe for de serviços')

    # valor do frete neste operação fiscal e Código da transportadora
    transportadora = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='transportadorasNF',
                                       help_text='Código da transportadora nesta operação fiscal')
    valor_frete = models.DecimalField("Valor do FRETE", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                      help_text='Valor do frete na nota fiscal de entrada ou de saida')
    valor_icm_frete = models.DecimalField("Valor do icms sobre o frete", max_length=16, max_digits=16, decimal_places=2,
                                          default=0.00, help_text='Valor do icms sobre o frete na nota fiscal de '
                                                                  'entrada ou de saida')
    cif_fob_frete = models.CharField("Indicador do tipo de frete", max_length=1, null=False,  default="1",
                                     choices=INDICADOR_FRETE_CHOICES,
                                     help_text='Indicador de frete. 0-Emitente, 1-Destinatário, 2-Terceiros, '
                                               '3-Próprio remetente, 4-Próprio destinatário, 9-Sem')
    tipo_frete = models.CharField("Indicador do custo do frete", max_length=1, null=False, default="1",
                                  choices=TIPO_FRETE_CHOICES,
                                  help_text='1 Frete na NFe COM crédito 2-Incluso na Nfe sem crédito 3-Conhec a parte '
                                            '4-Conhec parte sem crédito')

    # Status de fechamento do pedido/nfe na empresa
    status_manifestacao = models.CharField(max_length=1, null=False, default="C",
                                           choices=STATUS_CONFERENCIA_CHOICES,
                                           help_text='Status de conferência na manifestação de destinatário para '
                                                     'efeito de liberação de produtos para venda')

    status_contabilidade = models.CharField(max_length=1, null=False, default="C",
                                            choices=STATUS_CONFERENCIA_CHOICES,
                                            help_text='Status de conferencia da NF  pela contabilidade informando '
                                                      'que nf está fiscalmente OK')

    status_financeiro = models.CharField(max_length=1, null=False, default="A",
                                         choices=STATUS_CONFERENCIA_CHOICES,
                                         help_text='Status de conferencia da NF  pelo departamento financeiro '
                                                   'informando que nf está financeiramente (contas a pagar) OK')

    status_precos = models.CharField(max_length=1, null=False, default="C",
                                     choices=STATUS_CONFERENCIA_CHOICES,
                                     help_text='Status de conferencia da NF  pelo departamento custos informando que '
                                               'nf está com preços e custos OK')

    status_expedicao = models.CharField(max_length=1, null=False, default="L",
                                        choices=STATUS_CONFERENCIA_CHOICES,
                                        help_text='Status de conferência da NF  pela expedição informando que nf '
                                                  'está com quantidades armazenadas OK')
    # "S" para que nf esteja totalizada OK  E SEM DIFERENÇA
    # "D" para NF com diferença e com saldo não atualizado

    status_diferenca = models.CharField(max_length=1, null=False, default="C",
                                        choices=STATUS_DIFERENCA_CHOICES,
                                        help_text='Status de conferencia dos valores na nota fiscal de entrada ou '
                                                  'saida para ver se há diferenças')
    ultima_alteracao = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.serie) + ' ' + str(self.subserie)

    class Meta:
        verbose_name = 'Cadastro de Pedido'
        verbose_name_plural = 'Cadastro de Pedidos'
        # index_together = [
        #     ['participante', 'data_movimento'],
        #     ['data_movimento', 'notafiscal'],
        #     ['notafiscal', 'participante']
        # ]


# ------------------------------------------------------------------------------------------------------------------
# itens do pedido
# ------------------------------------------------------------------------------------------------------------------
class PedidoNfItem(models.Model):
    pedidonf = models.ForeignKey(PedidoNf, on_delete=models.CASCADE)
    sequencia = models.PositiveIntegerField("Sequência do item", null=False, default=1,
                                            help_text='Informe valor numerico e maior que zero para Número de item do '
                                                      'pedido 001 a 999 itens por nota fiscal')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    unidade = models.CharField(max_length=13, null=False, default=" ",
                               help_text='Unidade do produto vendido conforme cadastro no momento da venda. '
                                         'A mesma do cadastro de produtos')

    descricao = models.CharField(max_length=60, null=False, default=" ",
                                 help_text='Descrição do produto vendido conforme cadastro no momento da venda. '
                                           'A mesma do cadastro de produtos')

    observacoes = models.CharField(max_length=40, null=False, default=" ",
                                   help_text='Observação para efeito de informação fiscal específica neste produto')

    # natureza da operação fiscal de base  ou cfop que indicará o tipo de operação
    # (cfop+data) (data+cfop)
    cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE,
                             help_text='natureza de operação fiscal especifica deste produto')

    codigo_ncm = models.ForeignKey(CodigoNcm, on_delete=models.CASCADE)

    codigo_cest = models.ForeignKey(CodigoCest, on_delete=models.CASCADE)

    # Orçamento/Devolução/Cancelado/Em análise crédito/Bloqueado/Faturado/quitado etc
    status_pedido_item = models.CharField("Status deste pedido", max_length=1, null=False, default="N",
                                          choices=STATUS_PEDIDO_ITEM_CHOICES,
                                          help_text='status do pedido Orçamento/Devolução/Cancelado/Em análise crédito/'
                                                    'Bloqueado/Faturado/quitado etc ')

    # Número da autorização para Faturamento
    autorizacao_faturamento = models.CharField("Número da autorização para Faturamento", max_length=20, null=False,
                                               help_text='Número da autorização de faturamento emitida pelo cliente '
                                                         'ou pelo fornecedor')
    autorizacao_numitem = models.PositiveIntegerField("Número do Pedido", null=False,
                                                      validators=[MaxValueValidator(99999)],
                                                      help_text='Informe Número do item autorizado a fatura na Af do '
                                                                'fornecedor')

    quantidade = models.DecimalField("Quantidade vendida de produtos", max_length=16, max_digits=16,
                                     decimal_places=6, default=0.00, validators=[quantidade_maior_que_zero],
                                     help_text='Quantidade vendida de produtos no pedido e nota fiscal de entrada ou '
                                               'de saida')

    peso_liquido = models.DecimalField("Peso líquido do produto", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='peso líquido deste produto ')
    peso_bruto = models.DecimalField("Peso bruto do produto", max_length=16, max_digits=16,
                                     decimal_places=6, default=0.00,
                                     help_text='peso bruto deste produto ')

    metro_cubico = models.DecimalField("metros cúbicos do produto", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='metros cúbicos do produto')

    # movimenta estoques - campo trazido do cadastro de CFOP mas que pode ser alterado
    # campo com "N" sempre que a nota fiscal estiver bloqueada para análise
    movimenta_estoques = models.CharField("Movimenta Estoques?", max_length=1, null=False,  default="N",
                                          choices=SIM_NAO_CHOICES,
                                          help_text='S para movimentar estoques e N para não movimentar')

    saldo_fisico = models.DecimalField("Saldo físico do produto após gravação do pedido", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='Saldo físico do produto após gravação')

    saldo_fiscal = models.DecimalField("Saldo físico do produto após gravação", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00,
                                       help_text='Saldo fiscal do produto após geração e gravação da nota fiscal '
                                                 'emitida ou recebida')

    preco_custo = models.DecimalField("Preço de custo calculado após gravação", max_length=16, max_digits=16,
                                      decimal_places=6, default=0.00,
                                      help_text='Preço de custo do produto após gravada da nota fiscal de entrada '
                                                'ou saida')
    preco_medio = models.DecimalField("Preço de custo médio calculado após gravação", max_length=16, max_digits=16,
                                      decimal_places=6, default=0.00,
                                      help_text='Preço de custo médio do produto após gravação da nota fiscal de '
                                                'entrada ou saida')
    preco_custo_nfe = models.DecimalField("Preço de custo calculado após gravação da NFe", max_length=16, max_digits=16,
                                          decimal_places=6, default=0.00,
                                          help_text='Preço de custo do produto após gravação da nota fiscal de entrada '
                                                    'ou saida')
    preco_medio_nfe = models.DecimalField("Preço de custo médio calculado após gravação da Nfe", max_length=16,
                                          max_digits=16, decimal_places=6, default=0.00,
                                          help_text='Preço de custo médio do produto após gravada a nota fiscal de '
                                                    'entrada ou saida')

    preco_unitario = models.DecimalField("Preço unitário  de venda", max_length=16, max_digits=16,
                                         decimal_places=6, default=0.00,
                                         help_text='Preço unitário de venda conforme negociação e configurações '
                                                   'do sistema')
    perc_desc = models.DecimalField("Percentual de descontos no produto", max_length=10, max_digits=10,
                                    decimal_places=6, default=0.00, help_text='Percentual de descontos nos produtos')

    custo_informado = models.DecimalField("Preço gerencial de venda", max_length=16, max_digits=16,
                                          decimal_places=6, default=0.00,
                                          help_text='Preço gerencial de venda conforme negociação para efeito de '
                                                    'cálculo de Preço de venda')

    # data de movimento lembrar (codigo + data) e (data+codigo) servirão para diversas operações no sistema
    data_movimento = models.DateTimeField('Data de Movimentação do produto', auto_now_add=True,
                                          help_text='Data de Movimentação do produto. Mesma data do pedido para '
                                                    'efeito de cálculo de saldos (Codigo+data)')
    # Código do participante (Cliente ou fornecedor) nesta operação fiscal -
    # participante+data) (data+participante) (participante+codigo) (codigo+participante)- relatorios extratos
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='fornecedoresNFItem',
                                     help_text='Código do participante (Cliente ou fornecedor) nesta operação fiscal')

    # Total bruto (sem descontos) dos  produtos no pedido
    total_produto = models.DecimalField("Total do Produto", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00,
                                        help_text='Total bruto (sem descontos) do produto no pedido')

    # valores de cálculo do IPI  - indicação de tributação de IPI 1=trib 2=Isento ou não tributado 3=
    modalidade_ipi = models.CharField("Modalidade de cálculo do IPI ?", max_length=1, null=False,  default="3",
                                      choices=MODALIDADE_IPI_CHOICES,
                                      help_text='Modalidade de cálculo da base Icms')
    situacao_tributaria_ipi = models.ForeignKey(SituacaoTribIpi, on_delete=models.CASCADE,
                                                null=False, help_text='Código da situação tributária quanto ao pis '
                                                                      'nesta operação fiscal')
    base_calc_ipi = models.DecimalField("Base de cálculo do IPI", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Base de cálculo do IPI=valor produtos - descontos')
    perc_ipi = models.DecimalField("Percentual do IPI", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                   help_text='Percentual do IPI a recolher.')
    perc_red_ipi = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                       decimal_places=6, default=0.00,
                                       help_text='Percentual de redução de base do IPI.')

    # 3 valor da operação/0 Margem Valor Agregado(%)/1 Pauta (Valor)/2 Preço Tabelado Máx.(vlr)
    modalidade_calculo = models.CharField("Modalidade de cálculo da base Icms?", max_length=1, null=False,  default="3",
                                          choices=MODALIDADE_CALC_ICMS_CHOICES,
                                          help_text='Modalidade de cálculo da base Icms')
    # indicação de tributação  de ICMS 1=trib 2=Isento ou não trib 3=
    modalidade_icms = models.CharField("Modalidade de cálculo da base Icms?", max_length=1, null=False,  default="3",
                                       choices=MODALIDADE_ICMS_CHOICES,
                                       help_text='Modalidade de cálculo da base Icms')
    situacao_tributaria_icms = models.ForeignKey(SituacaoTribIcms, on_delete=models.CASCADE,
                                                 null=False, help_text='Código da situação tributária quanto ao Icms '
                                                                       'nesta operação fiscal')
    base_calc_icms = models.DecimalField("Base de cálculo do ICMS", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Base de cálculo do ICMS.')
    perc_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                    help_text='Percentual redução de base calc Icms.')
    perc_antec_tributaria = models.DecimalField("Percentual de antecipação tributária do ICMS", max_length=10,
                                                max_digits=10, decimal_places=6, default=0.00,
                                                help_text='Percentual de antecipação tributária do ICMS para efeito '
                                                          'de cálculo do custo de entrada')
    perc_red_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6,
                                        default=0.00, help_text='Percentual redução de base calc Icms.')

    # 3 valor da operação/0 Margem Valor Agregado(%)/1 Pauta (Valor)/2 Preço Tabelado Máx.(vlr)
    modalidade_calculo_subst = models.CharField("Modalidade de cálculo da base Icms Substituído?", max_length=1,
                                                null=False,  default="3", choices=MODALIDADE_ICMSSUB_CHOICES,
                                                help_text='Modalidade de cálculo da base Icms Substituído')
    base_calc_icms_sub = models.DecimalField("Base de cálculo do Icms Substituição", max_length=16,
                                             max_digits=16, decimal_places=2, default=0.00)
    perc_mva_sub = models.DecimalField("Percentual do MVA", max_length=10, max_digits=10, decimal_places=6,
                                       default=0.00, help_text='MVA para efeito de cálculo da base de icms substituição'
                                                               ' tributária')
    perc_icms_sub = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6,
                                        default=0.00, help_text='Percentual redução de base calc Icms.')
    perc_reducao_icms_sub = models.DecimalField("Percentual de reducao do ICMS Sub", max_length=10, max_digits=10,
                                                decimal_places=6, default=0.00,
                                                help_text='Percentual redução de base cálculo Icms substituição '
                                                          'tributária.')

    base_calc_antecipacao_trib = models.DecimalField("Base de cálculo da antecipação tributária se houver.",
                                                     max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                                     help_text='Base de cálculo da antecipação tributária se houver.')
    perc_antecipacao_trib = models.DecimalField("% para cálculo da antecipação tributária se houver.", max_length=10,
                                                max_digits=10, decimal_places=6, default=0.00,
                                                help_text='% para cálculo da antecipação tributária se houver.')

    situacao_tributaria_pis = models.ForeignKey(SituacaoTribPis, on_delete=models.CASCADE,
                                                null=False, help_text='Código da situação tributária quanto ao pis '
                                                                      'nesta operação fiscal')
    base_calc_pis = models.DecimalField("Valor Base de cálculo do Pis", max_length=16,
                                        max_digits=16, decimal_places=2, default=0.00,
                                        help_text='Valor Base de cálculo do Pis')
    perc_pis = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                   decimal_places=6, default=0.00,
                                   help_text='Percentual de redução de base do IPI.')

    # Código da Base de Cálculo do Crédito apurado no período, conforme a Tabela 4.3.7. SPED PIS COFINS
    # TODO natureza_base_pis = models.ForeignKey(NaturezaBasePis, on_delete=models.CASCADE)
    # tabela 4.3.6 - Tabela Código de Tipo de Crédito - Atualizada em 03/01/2012 : REGISTRO M500: CRÉDITO DE COFINS
    # RELATIVO AO PERÍODO
    # TODO tipo_credito_base_pis = models.ForeignKey(CódigoTipoCreditoPis, on_delete=models.CASCADE)
    situacao_tributaria_cofins = models.ForeignKey(SituacaoTribCofins, on_delete=models.CASCADE,
                                                   help_text='Código da situação tributária quanto ao Cofins nesta '
                                                             'operação fiscal')
    base_calc_cofins = models.DecimalField("Valor Base de cálculo do cofins", max_length=16, max_digits=16,
                                           decimal_places=2, default=0.00,
                                           help_text='Valor Base de cálculo do cofins')

    perc_fundo_pobreza = models.DecimalField("Percentual para fundo de combate a pobreza", max_length=10, max_digits=10,
                                             decimal_places=6, default=0.00,
                                             help_text='Percentual para fundo de combate a pobreza')
    # LEI DA TAANSPARÊNCIA FISCAL NOTA TÉCNICA 003 2013 % DE TRIBUTOS TOTAL NESTE ITEM
    perc_trib_aproximado = models.DecimalField("Percentual", max_length=10, max_digits=10,
                                               decimal_places=6, default=0.00,
                                               help_text='Percentual aproximado de tributação  conforme lei '
                                                         'transparência fiscal')

    base_calc_import = models.DecimalField("Valor Base de cálculo do imposto sobre importação", max_length=16,
                                           max_digits=16, decimal_places=2, default=0.00,
                                           help_text='Valor Base de cálculo do imposto sobre importação')
    perc_import = models.DecimalField("Percentual de II imposto sobre importação", max_length=10, max_digits=10,
                                      decimal_places=6, default=0.00,
                                      help_text='Percentual de II imposto sobre importação')

    # valor dos serviços se nfe for de serviços
    base_calc_issqn = models.DecimalField("Base de cálculo serviços", max_length=16, max_digits=16, decimal_places=2,
                                          default=0.00, help_text='valor Base de cálculo serviços se nfe for de '
                                                                  'serviços')
    perc_issqn = models.DecimalField("Percentual do ISS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                     help_text='Percentual do ISS a recolher.')

    # % das despesas acessórias para rateio por item
    perc_desp_acessorias = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                               decimal_places=6, default=0.00,
                                               help_text='Percentual de redução de base do IPI.')
    perc_seguro = models.DecimalField("Percentual de seguro neste Produto", max_length=10, max_digits=10,
                                      decimal_places=6, default=0.00, help_text='Percentual de seguro ')
    perc_frete = models.DecimalField("Percentual de frete", max_length=10, max_digits=10, decimal_places=6,
                                     default=0.00, help_text='Percentual de frete ')

    # Natureza de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    natureza_custos = models.ForeignKey(NaturezaCusto, default=1, on_delete=models.CASCADE,
                                        help_text='Natureza de custos deste tipo de operação de venda ou para qual '
                                                  'conta de custos sistema irá')

    # Centro de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    centro_custos = models.ForeignKey(CentroCusto, default=1, on_delete=models.CASCADE,
                                      help_text='Centro de custos deste tipo de operação de venda ou para qual conta '
                                                'de custos sistema irá')

    # Código da promoção no cadastro de produtos corrente quando foi feita esta venda
    codigo_promocao = models.ForeignKey(ProdutoPromocao, default=0, on_delete=models.CASCADE,
                                        help_text='Código da promoção desta venda na hora da venda')
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.pedido) + ' ' + str(self.item) + ' ' + str(self.produto)

    class Meta:
        unique_together = ("pedidonf", "sequencia", "produto")
        verbose_name = 'Cadastro de Pedido'
        verbose_name_plural = 'Cadastro de Pedidos'


# ----------------------------------------------------------------------------------------------------------------------
# PEDIDOS DE VENDAS ORÇAMENTOS ENCOMENDAS REQUISIÇÕES ETC (KCEI03)
# ----------------------------------------------------------------------------------------------------------------------
class PedidoWeb(models.Model):
    # id do será o Número do pedido
    # Série será as 3 primeiras letras do Código da empresa
    # subserie conforme operação "VEN" "ORC" "ETC"
    serie = models.CharField("Série", max_length=3, null=False, default='MAT')
    subserie = models.CharField("Subsérie", max_length=3, null=False, default='WEB')

    # informação deve ser trazida da tabela TipoDocumento
    indicador_pagamento_nfe = models.CharField("Indicador da forma de pagamento", max_length=1, null=False, default="0",
                                               choices=INDICADOR_PAGAMENTO_CHOICES,
                                               help_text='Indicador da forma de pagamento para informação na nota '
                                                         'fiscal eletrônica')

    # Orçamento/Devolução/Cancelado/Em análise crédito/Bloqueado/Faturado/quitado Aprovado para faturamento
    status_pedido = models.CharField("Status deste pedido", max_length=1, null=False, default="W",
                                     choices=STATUS_PEDIDO_ITEM_CHOICES,
                                     help_text='status do pedido Orçamento/Devolução/Cancelado/Em análise crédito/'
                                               'Bloqueado/Faturado/quitado etc ')

    # Código do regime Tributário do emitente ou do fornecedor 1-Simples na 2-Simples exc  3-Normal
    regime_tributario = models.CharField("Regime Tributário Emitente", max_length=1, null=False, default="1",
                                         choices=REGIME_TRIBUTARIO_CHOICES,
                                         help_text='código do regime tributário do emitente ou do fornecedor '
                                                   '1-Simples na 2-Simples exc  3-Normal')

    notafiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, null=True, blank=True,
                                   help_text='Número da nota fiscal emitida para este pedido conforme Número no '
                                             'faturamento da NFe ou NFce')

    # Número da autorização para Faturamento
    autorizacao_faturamento = models.CharField("Número da autorização para Faturamento", max_length=20, null=True,
                                               blank=True, help_text='Número da autorização de faturamento emitida '
                                                                     'pelo cliente ou pelo fornecedor')

    autorizacao_numitem = models.PositiveIntegerField("Número do Pedido", default=0)

    # Indicador de emitente do documento fiscal
    indicador_emitente = models.CharField("Indicador de emitente da NFe", max_length=1, null=True,
                                          choices=EMISSAO_CHOICES, default="1",
                                          help_text='Indicador de emitente do documento fiscal  0_Emissão própria '
                                                    '1_Terceiros')

    # 00|Doc regular| 01|Doc reg extemporâneo| 02|Doc cancelado|  03|Doc canc extemporâneo| 04|NFe denegada|
    # 05|NFe Numeração inutilizada| 06|Doc Fiscal Compl| 07|Doc Fiscal Compl extemporâneo| 08|Doc RegEspecial
    # Situação da nota fiscal quanto ao cancelamento (item 4.1.2- Tabela Situação do Documento do AtoCOTEPE/ICMS nº 09,
    #  de 2008),
    # situacaodocumentosped = models.ForeignKey(SituacaoDocumentoSped, on_delete=models.CASCADE, null=False, default=1,
    #                                           help_text='Situação Do Documento Fiscal conforme tabela 4.1.2 do Sped')

    situacaodocumentosped = models.PositiveIntegerField(default=1)

    # TODO  Depois tem que mudar para 55
    modelodocumentofiscal = models.PositiveIntegerField(default=1)

    # modelodocumentofiscal = models.ForeignKey(ModeloDocumentoFiscal, on_delete=models.CASCADE, null=False, default=1,
    #                                           help_text='Código Do Documento Fiscal conforme tabela Sped -
    # Ex. 55|Nota'
    #                                                     ' Fiscal Eletrônica')

    data_pedido = models.DateField('Data do Pedido', null=False, blank=False, auto_now_add=True)
    data_emissao = models.DateField('Data de De Emissão da Nfe', null=False, blank=False, auto_now_add=True)
    data_saida = models.DateTimeField('Data de saida para entrega', null=False, blank=False, auto_now_add=True)
    data_movimento = models.DateTimeField('Data de Movimentação da Nfe', null=False, blank=False, auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    # natureza da operação fiscal de base  ou cfop principal que indicará o tipo de saida (nos itens tem vários)
    # TODO Takes out null=True e blank=True
    cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE, blank=True, null=True,
                             help_text='Informe o Cfop - Código fiscal de Operação')

    # tipo de pagamento utilizado neste pedido
    tipo_de_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.CASCADE, default=1,
                                          related_name='tipopagamentoWeb')

    # Prazos para pagamento
    prazo_de_pagamento = models.ForeignKey(PrazoPagamento, on_delete=models.CASCADE, default=1)

    # Código do participante (Cliente ou fornecedor) nesta operação fiscal
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='clienteWeb')

    # vendedor responsável pela venda ou comprador
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendedor')

    # mensagem padrao a ser impressa durante a emissão da nota fiscal como observações adicionais na NF
    mensagempadrao = models.ForeignKey(MensagemPadrao, on_delete=models.CASCADE, null=True,
                                       help_text='mensagem padrão a ser impressa durante a emissão da nota fiscal '
                                                 'como observações adicionais na NF')

    # Tipo de movimentação de entrada ou saida
    # TODO Depois tornar preenchimento obrigatório
    tipo_pedido = models.ForeignKey(PedidoTipo, on_delete=models.CASCADE, null=True, blank=True,
                                    help_text='Informe Tipo de movimentação de entrada ou saida')

    # indPres (nfe 3.10) Indicador de presença do comprador no estabelecimento ----
    indicador_presenca_nfe = models.CharField("Indicador de presença do comprador NFe", max_length=1, null=False,
                                              choices=INDICA_PRESENCA_CHOICES, default="1",
                                              help_text='indPres (nfe 3.10) Indicador de presença do comprador no '
                                                        'estabelecimento comercial no momento da operação')

    # Tipo de Preço usado na saida de pedidos da tabela
    tipo_preco_pedido = models.CharField(max_length=1, null=False, default="V",
                                         help_text='Tipo de Preço usado na saida de pedidos V Preço VENDA / '
                                                   'C Último CUSTO / I Preço indexado, etc')

    # Total bruto (sem descontos) dos  produtos no pedido
    total_produtos = models.DecimalField("Total dos Produtos", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Total bruto (sem descontos) dos  produtos no '
                                                                 'pedido')
    # Percentual  % desconto total na Nf para rateio por item nos itens
    perc_desc = models.DecimalField("Percentual de descontos nos produtos", max_length=10, max_digits=10,
                                    decimal_places=6, default=0.00, help_text='Percentual de descontos nos produtos')
    # valor do desconto na nota fiscal em totais (valor dos descontos em % + valor dos descontos em valores do pedido)
    descont_valor = models.DecimalField("Valor desconto no Pedido", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='valor do desconto na nota fiscal em totais (valor dos '
                                                                'descontos em % + valor dos descontos em valores do '
                                                                'pedido')

    # valores de cálculo do IPI
    base_calc_ipi = models.DecimalField("Base de cálculo do IPI", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Base de cálculo do IPI')
    valor_ipi = models.DecimalField("Valor do IPI", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                    help_text='Valor calculado do IPI a recolher.')
    perc_ipi = models.DecimalField("Percentual do IPI", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                   help_text='Percentual do IPI a recolher.')

    # Total líquido do pedido (somatório dos produtos - descontos + impostos + frete + outros valores)
    valor_contabil = models.DecimalField("Total líquido do Pedido", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00,
                                         help_text='Total líquido do pedido/total líquido da Nota fiscal pedido.')

    base_calc_icms = models.DecimalField("Base de cálculo do ICMS", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Base de cálculo do ICMS.')
    valor_icms = models.DecimalField("Valor do ICMS", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                     help_text='Valor calculado do ICMS a recolher.')
    perc_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                    help_text='Percentual do ICMS a recolher.')

    # valores de cálculo do ICMS substituição tributária
    # valor do icms a recolher calculado=valor_icms_sub - valor_icms
    base_calc_icms_sub = models.DecimalField("Base de cálculo do Icms Substituição", max_length=16,
                                             max_digits=16, decimal_places=2, default=0.00,
                                             help_text='Base de cálculo do Icms Substituição tributária')
    valor_icms_sub = models.DecimalField("Valor do ICMS substituição tributária", max_length=16,
                                         max_digits=16, decimal_places=2, default=0.00,
                                         help_text='Valor do ICMS substituição tributária')

    # valor das despesas acessórias para rateio por item
    valor_despesas_acess = models.DecimalField("Valor despesas acessorias", max_length=16,
                                               max_digits=16, decimal_places=2, default=0.00,
                                               help_text='Valor das despesas acessorias')

    # valor do pis para rateio por item
    base_calc_pis = models.DecimalField("Valor Base de cálculo do Pis", max_length=16,
                                        max_digits=16, decimal_places=2, default=0.00,
                                        help_text='Valor Base de cálculo do Pis')

    valor_pis = models.DecimalField("Valor do Pis", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                    help_text='Valor do pis')

    # valor do cofins para rateio por item
    base_calc_cofins = models.DecimalField("Valor Base de cálculo do cofins", max_length=16,
                                           max_digits=16, decimal_places=2, default=0.00,
                                           help_text='Valor Base de cálculo do cofins')
    valor_cofins = models.DecimalField("Valor do cofins", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                       help_text='Valor do cofins')

    # valor do seguro
    valor_seguro = models.DecimalField("Valor do cofins", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                       help_text='Valor do cofins')

    # valor dos serviços se nfe for de serviços
    base_calc_issqn = models.DecimalField("Base de cálculo serviços", max_length=16,
                                          max_digits=16, decimal_places=2, default=0.00,
                                          help_text='valor Base de cálculo serviços se nfe for de serviços')
    perc_issqn = models.DecimalField("Percentual do ISS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                     help_text='Percentual do ISS a recolher.')
    quantidade_servicos = models.DecimalField("Quantidade de serviços", max_length=10,
                                              max_digits=10, decimal_places=6, default=0.00,
                                              help_text='Quantidade dos serviços se nfe for de serviços')
    valor_servicos = models.DecimalField("Valor dos serviços", max_length=16, max_digits=16,
                                         decimal_places=2, default=0.00,
                                         help_text='valor dos serviços se nfe for de serviços')

    # valor do frete neste operação fiscal e Código da transportadora
    transportadora = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='transportadoraWeb',
                                       help_text='Código da transportadora nesta operação fiscal')
    valor_frete = models.DecimalField("Valor do FRETE", max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                      help_text='Valor do frete na nota fiscal de entrada ou de saida')
    valor_icm_frete = models.DecimalField("Valor do icms sobre o frete", max_length=16, max_digits=16,
                                          decimal_places=2, default=0.00,
                                          help_text='Valor do icms sobre o frete na nota fiscal de entrada ou de saida')
    cif_fob_frete = models.CharField("Indicador do tipo de frete", max_length=1, null=False,  default="1",
                                     choices=INDICADOR_FRETE_CHOICES,
                                     help_text='Indicador de frete. 0-Emitente, 1-Destinatário , 2-Terceiros, 3-Próprio'
                                               ' remetente, 4-próprio destinatário, 9-Sem')
    tipo_frete = models.CharField("Indicador do custo do frete", max_length=1, null=False, default="1",
                                  choices=TIPO_FRETE_CHOICES,
                                  help_text='1 Frete na NFe COM cre 2-Incluso na Nfe sem crédito 3-Conhec a parte '
                                            '4-Conhec parte sem cred')

    status_manifestacao = models.CharField(max_length=1, null=False, default="C",
                                           choices=STATUS_CONFERENCIA_CHOICES,
                                           help_text='Status de conferencia na manifestação de destinatário para efeito'
                                                     ' de liberação de produtos para venda')

    status_contabilidade = models.CharField(max_length=1, null=False, default="C",
                                            choices=STATUS_CONFERENCIA_CHOICES,
                                            help_text='Status de conferencia da NF  pela contabilidade informando que '
                                                      'nf está fiscalmente OK')

    status_financeiro = models.CharField(max_length=1, null=False, default="A",
                                         choices=STATUS_CONFERENCIA_CHOICES,
                                         help_text='Status de conferencia da NF  pelo departamento financeiro '
                                                   'informando que nf está financeiramente (contas a pagar) OK')

    status_precos = models.CharField(max_length=1, null=False, default="C",
                                     choices=STATUS_CONFERENCIA_CHOICES,
                                     help_text='Status de conferencia da NF  pelo departamento custos informando que '
                                               'nf está com preços e custos OK')

    status_expedicao = models.CharField(max_length=1, null=False, default="L", choices=STATUS_CONFERENCIA_CHOICES,
                                        help_text='Status de conferencia da NF  pela expedição informando que nf está '
                                                  'com quantidades armazenadas OK')
    # "S" para que nf esteja totalizada OK  E SEM DIFERENCA
    # "D" para NF com diferenca e com saldo não atualizado

    status_diferenca = models.CharField(max_length=1, null=False, default="C",
                                        choices=STATUS_DIFERENCA_CHOICES,
                                        help_text='Status de conferencia dos valores na nota fiscal de entrada ou '
                                                  'saida para ver se há diferenças ')

    observacoes = models.TextField("Observações", max_length=200, null=True, blank=True)
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('materiais:pedidoweb_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id) + ' ' + str(self.serie) + ' ' + str(self.subserie)

    def total_preco_unitario(self):
        return str(sum(pedidowebitem.tot_preco_unitario() for pedidowebitem in self.pedidowebitem_set.all()))

    def pode_alterar_pedido(self):
        if self.status_pedido == 'W':
            return True
        else:
            return False

    class Meta:
        ordering = ['-id']
        verbose_name = 'Cadastro de Pedido'
        verbose_name_plural = 'Cadastro de Pedidos'
        index_together = [
            ['participante', 'data_movimento'],
            ['data_movimento', 'notafiscal'],
            ['notafiscal', 'participante']
        ]


# ------------------------------------------------------------------------------------------------------------------
# itens do pedido
# ------------------------------------------------------------------------------------------------------------------
class PedidoWebItem(models.Model):
    pedidoweb = models.ForeignKey(PedidoWeb, on_delete=models.CASCADE)
    sequencia = models.PositiveIntegerField("Sequência do item", null=False, default=1)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    unidade = models.CharField(max_length=13, null=False, default=" ",
                               help_text='Unidade do produto vendido conforme cadastro no momento da venda. A mesma '
                                         'do cadastro de produtos')

    descricao = models.CharField(max_length=60, null=False, default=" ",
                                 help_text='Descrição do produto vendido conforme cadastro no momento da venda. A '
                                           'mesma do cadastro de produtos')

    observacoes = models.CharField(max_length=40, null=True, blank=True, default=" ",
                                   help_text='Observação para efeito de informação fiscal específica neste produto')

    # natureza da operação fiscal de base  ou cfop que indicará o tipo de operação
    # (cfop+data) (data+cfop)
    # TODO CFOP Resolver depois
    # cfop = models.ForeignKey(Cfop, on_delete=models.CASCADE, default=1,
    #                         help_text='natureza de operação fiscal específica deste produto')
    cfop = models.IntegerField(default=5102)

    # TODO CFOP Resolver depois
    # codigo_ncm = models.ForeignKey(CodigoNcm, on_delete=models.CASCADE, default=1)
    codigo_ncm = models.CharField(max_length=100)

    # TODO CFOP Resolver depois
    # codigo_cest = models.ForeignKey(CodigoCest, on_delete=models.CASCADE, default=1)
    codigo_cest = models.IntegerField()

    # Orçamento / Devolução / Cancelado / Em análise crédito/ Bloqueado/ Faturado / quitado etc
    status_pedido_item = models.CharField("Status deste pedido", max_length=1, null=False, default="N",
                                          choices=STATUS_PEDIDO_ITEM_CHOICES,
                                          help_text='status do pedido Orçamento / Devolução /Cancelado /Em análise '
                                                    'crédito /Bloqueado/ Faturado / quitado etc ')

    # Número da autorização para Faturamento
    autorizacao_faturamento = models.CharField("Número da autorização para Faturamento", max_length=20,
                                               null=True, blank=True,
                                               help_text='Número da autorização de faturamento emitida pelo cliente '
                                                         'ou pelo fornecedor')
    autorizacao_numitem = models.PositiveIntegerField("Número do Pedido", default=0,
                                                      validators=[MaxValueValidator(99999)])

    quantidade = models.DecimalField("Quantidade", max_length=16, max_digits=16, decimal_places=6,
                                     default=1, validators=[quantidade_maior_que_zero],
                                     help_text='Quantidade vendida de produtos no pedido e nota fiscal de entrada ou '
                                               'de saida')

    peso_liquido = models.DecimalField("Peso líquido do produto", max_length=16, max_digits=16, decimal_places=6,
                                       default=0.00, help_text='peso líquido deste produto')
    peso_bruto = models.DecimalField("Peso bruto do produto", max_length=16, max_digits=16, decimal_places=6,
                                     default=0.00, help_text='peso bruto deste produto')

    metro_cubico = models.DecimalField("metros cúbicos do produto", max_length=16, max_digits=16, decimal_places=6,
                                       default=0.00, help_text='metros cúbicos do produto')

    # movimenta estoques - campo trazido do cadastro de CFOP mas que pode ser alterado
    # campo com "N" sempre que a n nota fiscal estiver bloqueada para análise
    movimenta_estoques = models.CharField("Movimenta Estoques?", max_length=1, null=False,  default="N",
                                          choices=SIM_NAO_CHOICES, help_text='S para movimentar estoques e N para nao '
                                                                             'movimentar')

    saldo_fisico = models.DecimalField("Saldo físico do produto após gravação do pedido", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00, help_text='Saldo físico do produto após '
                                                                                 'gravação')

    saldo_fiscal = models.DecimalField("Saldo físico do produto após gravação", max_length=16, max_digits=16,
                                       decimal_places=6, default=0.00, help_text='Saldo fiscal do produto após '
                                                                                 'geração e gravação da nota fiscal '
                                                                                 'emitida ou recebida')

    preco_custo = models.DecimalField("Preço de custo calculado após gravação", max_length=16, max_digits=16,
                                      decimal_places=6, default=0.00,
                                      help_text='Preço de custo do produto após gravação da nota fiscal de entrada '
                                                'ou saida')
    preco_medio = models.DecimalField("Preço de custo médio calculado após gravação", max_length=16, max_digits=16,
                                      decimal_places=6, default=0.00,
                                      help_text='Preço de custo médio do produto após gravação da nota fiscal de '
                                                'entrada ou saida')
    preco_custo_nfe = models.DecimalField("Preço de custo calculado após gravação da NFe", max_length=16, max_digits=16,
                                          decimal_places=6, default=0.00,
                                          help_text='Preço de custo do produto após gravação da nota fiscal de '
                                                    'entrada ou saida')
    preco_medio_nfe = models.DecimalField("Preço de custo médio calculado após gravação da Nfe", max_length=16,
                                          max_digits=16, decimal_places=6, default=0.00,
                                          help_text='Preço de custo médio do produto após gravação a nota fiscal de '
                                                    'entrada ou saida')

    preco_unitario = models.DecimalField("Preço Unitário", max_length=16, max_digits=16,
                                         decimal_places=6, default=0.00,
                                         help_text='Preço unitário de venda conforme negociação e configurações do '
                                                   'sistema')
    perc_desc = models.DecimalField("% Desc", max_length=10, max_digits=10,
                                    decimal_places=6, default=0.00, help_text='Percentual de descontos nos produtos')

    custo_informado = models.DecimalField("Preço gerencial de venda", max_length=16, max_digits=16,
                                          decimal_places=6, default=0.00,
                                          help_text='Preço gerencial de venda conforme negociação para efeito de '
                                                    'cálculo de Preço de venda')

    # data de movimento lembrar (codigo + data) e (data+codigo) servirão para diversas operações no sistema
    data_movimento = models.DateTimeField('Data de Movimentação do produto', null=False, blank=False, auto_now_add=True,
                                          help_text='Data de Movimentação do produto. Mesma data do pedido para '
                                                    'efeito de cálculo de saldos (Codigo+data)')
    # Código do participante (Cliente ou fornecedor) nesta operação fiscal -
    # participante+data) (data+participante) (participante+codigo) (codigo+participante)- relatórios extratos
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='fornecedoresWeb',
                                     blank=True, null=True, help_text='Código do Participante')

    # Total bruto (sem descontos) dos  produtos no pedido
    total_produto = models.DecimalField("Total do Produto", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Total bruto (sem descontos) do produto no pedido')

    # valores de cálculo do IPI  - indicação de tributação  de IPI 1=trib 2=Isento ou não trib 3=
    modalidade_ipi = models.CharField("Modalidade de cálculo do IPI ?", max_length=1, null=False,  default="3",
                                      choices=MODALIDADE_IPI_CHOICES,
                                      help_text='Modalidade de cálculo da base Icms')
    # TODO Resolver depois
    # situacao_tributaria_ipi = models.ForeignKey(SituacaoTribIpi, on_delete=models.CASCADE, default=1,
    #                                             help_text='Código da situação tributária quanto ao pis nesta
    # operação fiscal')
    situacao_tributaria_ipi = models.IntegerField()
    base_calc_ipi = models.DecimalField("Base de cálculo do IPI", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00,
                                        help_text='Base de cálculo do IPI=valor produtos - descontos')
    perc_ipi = models.DecimalField("Percentual do IPI", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                   help_text='Percentual do IPI a recolher.')
    perc_red_ipi = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                       decimal_places=6, default=0.00,
                                       help_text='Percentual de redução de base do IPI.')

    # 3 valor da operação/0 Margem Valor Agregado(%)/1 Pauta (Valor)/2 Preço Tabelado Máx.(valor)
    modalidade_calculo = models.CharField("Modalidade de cálculo da base Icms?", max_length=1, null=False,  default="3",
                                          choices=MODALIDADE_CALC_ICMS_CHOICES,
                                          help_text='Modalidade de cálculo da base Icms')

    # indicação de tributação de ICMS 1=tributado 2=Isento ou não tributado 3=
    modalidade_icms = models.CharField("Modalidade de cálculo da base Icms?", max_length=1, null=False,  default="3",
                                       choices=MODALIDADE_ICMS_CHOICES,
                                       help_text='Modalidade de cálculo da base Icms')

    # TODO Resolver depois
    # situacao_tributaria_icms = models.ForeignKey(SituacaoTribIcms, on_delete=models.CASCADE, default=1,
    #                                              help_text='Código da situação tributária quanto ao Icms nesta '
    #                                                        'operação fiscal')
    situacao_tributaria_icms = models.IntegerField()

    base_calc_icms = models.DecimalField("Base de cálculo do ICMS", max_length=16, max_digits=16, decimal_places=2,
                                         default=0.00, help_text='Base de cálculo do ICMS.')
    perc_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                    help_text='Percentual redução de base calc Icms.')
    perc_antec_tributaria = models.DecimalField("Percentual de antecipação tributária do ICMS", max_length=10,
                                                max_digits=10, decimal_places=6, default=0.00,
                                                help_text='Percentual de antecipação tributária do ICMS para efeito '
                                                          'de cálculo do custo de entrada')
    perc_red_icms = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6,
                                        default=0.00, help_text='Percentual redução de base calc Icms.')

    # 3 valor da operação/0 Margem Valor Agregado(%)/1 Pauta (Valor)/2 Preço Tabelado Máx.(vlr)
    modalidade_calculo_subst = models.CharField("Modalidade de cálculo da base Icms substituído?", max_length=1,
                                                null=False,  default="3", choices=MODALIDADE_ICMSSUB_CHOICES,
                                                help_text='Modalidade de cálculo da base Icms substituído')
    base_calc_icms_sub = models.DecimalField("Base de cálculo do Icms Substituição", max_length=16,
                                             max_digits=16, decimal_places=2, default=0.00)
    perc_mva_sub = models.DecimalField("Percentual do MVA", max_length=10, max_digits=10, decimal_places=6,
                                       default=0.00, help_text='MVA para efeito de cálculo da base de icms '
                                                               'substituição tributária')
    perc_icms_sub = models.DecimalField("Percentual do ICMS", max_length=10, max_digits=10, decimal_places=6,
                                        default=0.00, help_text='Percentual redução de base cálculo Icms.')
    perc_reducao_icms_sub = models.DecimalField("Percentual de reducao do ICMS Sub", max_length=10, max_digits=10,
                                                decimal_places=6, default=0.00,
                                                help_text='Percentual redução de base calc Icms substituição '
                                                          'tributária')

    base_calc_antecipacao_trib = models.DecimalField("Base de cálculo da antecipação tributária se houver.", 
                                                     max_length=16, max_digits=16, decimal_places=2, default=0.00,
                                                     help_text='Base de cálculo da antecipação tributária se houver.')
    perc_antecipacao_trib = models.DecimalField("% para cálculo da antecipação tributária se houver.", max_length=10, 
                                                max_digits=10, decimal_places=6, default=0.00, 
                                                help_text='% para cálculo da antecipação tributária se houver.')

    # TODO Resolver depois
    # situacao_tributaria_pis = models.ForeignKey(SituacaoTribPis, on_delete=models.CASCADE, default=1,
    #                                             null=False, help_text='Código da situação tributária quanto ao pis '
    #                                                                   'nesta operação fiscal')
    situacao_tributaria_pis = models.IntegerField()

    base_calc_pis = models.DecimalField("Valor Base de cálculo do Pis", max_length=16, max_digits=16, decimal_places=2,
                                        default=0.00, help_text='Valor Base de cálculo do Pis')
    perc_pis = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10, 
                                   decimal_places=6, default=0.00, help_text='Percentual de redução de base do IPI.')

    # Código da Base de Cálculo do Crédito apurado no período, conforme a Tabela 4.3.7. SPED PIS COFINS
    # TODO FALTA CRIAR A CLASSE NaturezaBasePis
    # natureza_base_pis = models.ForeignKey(NaturezaBasePis, on_delete=models.CASCADE, null=True, blank=True)
    # tabela 4.3.6 - Tabela Código de Tipo de Crédito - Atualizada em 03/01/2012 : REGISTRO M500: CRÉDITO DE COFINS 
    # RELATIVO AO PERÍODO
    # TODO tipo_credito_base_pis = models.ForeignKey(CódigoTipoCreditoPis, on_delete=models.CASCADE)

    # TODO Resolver depois
    # situacao_tributaria_cofins = models.ForeignKey(SituacaoTribCofins, on_delete=models.CASCADE, default=1,
    #                                                help_text='Código da situação tributária quanto ao Cofins nesta '
    #                                                          'operação fiscal')
    situacao_tributaria_cofins = models.IntegerField()

    base_calc_cofins = models.DecimalField("Valor Base de cálculo do cofins", max_length=16, max_digits=16,
                                           decimal_places=2, default=0.00, help_text='Valor Base de cálculo do cofins')

    perc_fundo_pobreza = models.DecimalField("Percentual para fundo de combate a pobreza", max_length=10, max_digits=10,
                                             decimal_places=6, default=0.00, help_text='Percentual para fundo de '
                                                                                       'combate a pobreza')
    # LEI DA TAANSPARÊNCIA FISCAL NOTA TÉCNICA 003 2013 % DE TRIBUTOS TOTAL NESTE ITEM
    perc_trib_aproximado = models.DecimalField("Percentual", max_length=10, max_digits=10,
                                               decimal_places=6, default=0.00,
                                               help_text='Percentual aproximado de tributação conforme lei '
                                                         'transparência fiscal')

    base_calc_import = models.DecimalField("Valor Base de cálculo do imposto sobre importação", max_length=16,
                                           max_digits=16, decimal_places=2, default=0.00,
                                           help_text='Valor Base de cálculo do imposto sobre importação')
    perc_import = models.DecimalField("Percentual de II imposto sobre importação", max_length=10, max_digits=10, 
                                      decimal_places=6, default=0.00, 
                                      help_text='Percentual de II imposto sobre importação')

    # valor dos serviços se nfe for de serviços
    base_calc_issqn = models.DecimalField("Base de cálculo serviços", max_length=16, max_digits=16, decimal_places=2,
                                          default=0.00, help_text='valor Base de cálculo serviços se nfe for '
                                                                  'de serviços')
    perc_issqn = models.DecimalField("Percentual do ISS", max_length=10, max_digits=10, decimal_places=6, default=0.00,
                                     help_text='Percentual do ISS a recolher.')

    # % das despesas acessórias para rateio por item
    perc_desp_acessorias = models.DecimalField("Percentual de redução de base do IPI", max_length=10, max_digits=10,
                                               decimal_places=6, default=0.00, help_text='Percentual de redução de '
                                                                                         'base do IPI.')
    perc_seguro = models.DecimalField("Percentual de seguro neste Produto", max_length=10, max_digits=10,
                                      decimal_places=6, default=0.00, help_text='Percentual de seguro ')
    perc_frete = models.DecimalField("Percentual de frete neste Produto", max_length=10, max_digits=10,
                                     decimal_places=6, default=0.00, help_text='Percentual de frete ')

    # Natureza de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    # natureza_custos = models.ForeignKey(NaturezaCusto, default=1,
    #                                     on_delete=models.CASCADE,
    #                                     help_text='Natureza de custos deste tipo de operação de venda ou para qual '
    #                                               'conta de custos sistema irá')

    natureza_custos = models.PositiveIntegerField(default=1)

    # Centro de custos deste tipo de operação de venda ou para qual conta de custos sistema irá
    # centro_custo = models.ForeignKey(CentroCusto, default=1, on_delete=models.CASCADE,
    #                                  help_text='Centro de custos deste tipo de operação de venda ou para qual conta '
    #                                            'de custos sistema irá')

    centro_custo = models.PositiveIntegerField(default=1)

    # Código da promoção no cadastro de produtos corrente quando foi feita esta venda
    # codigo_promocao = models.ForeignKey(ProdutoPromocao, default=1, on_delete=models.CASCADE,
    #                                    help_text='Código da promoção desta venda na hora da venda')
    # TODO Resolver se vai ser obrigatório ou nao o preenchimento desse campo
    codigo_promocao = models.IntegerField(null=True, blank=True, default=0)
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.pedidoweb)

    def tot_preco_unitario(self):
        return self.preco_unitario

    class Meta:
        ordering = ['sequencia']
        unique_together = ("pedidoweb", "sequencia", "produto")
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Itens de Pedidos'


# ------------------------------------------------------------------------------------------------------------------
# dados da garantia do pedido
# ------------------------------------------------------------------------------------------------------------------
class PedidoGarantia(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    data_garantia = models.DateField('Data de Emissão da Nfe', null=False, blank=False)

    numero_garantia = models.CharField(max_length=1, null=False, default=" ", help_text='Número do certificado de '
                                                                                        'garantia do produto ')
