from django.core.exceptions import ValidationError

DEBITO_CREDITO_CHOICES = (
                          ('D', 'Débito'),
                          ('C', 'Crédito')
                          )

FISICA_JURIDICA_CHOICES = (
                           ('F', 'Pessoa Física'),
                           ('J', 'Pessoa Jurídica')
                           )

MES_COMPETENCIA_CHOICES = (
                           (1, 'Janeiro'), 
                           (2, 'Fevereiro'), 
                           (3, 'Março'), 
                           (4, 'Abril'), 
                           (5, 'Maio'), 
                           (6, 'Junho'),
                           (7, 'Julho'), 
                           (8, 'Agosto'), 
                           (9, 'Setembro'), 
                           (10, 'Outubro'), 
                           (11, 'Novembro'),
                           (12, 'Dezembro')
                        )

COMPETENCIA_STATUS_CHOICES = (
                  ('A', 'Aberta'),
                  ('F', 'Fechada'),
                  ('B', 'Bloqueada pela Contabildade')
                  )


RECEITA_DESPESA_CHOICES = (
                           ('R', 'Receita'),
                           ('C', 'Custos'),
                           ('D', 'Despesas'),
                           )

SIM_NAO_CHOICES = (
                   ('S', 'Sim'),
                   ('N', 'Não'),
                   )


TIPO_CONTA_CHOICES = (
                      ('A', 'Analítica'),
                      ('S', 'Sintética'),
                      ('G', 'Grupo'),
                      )

TIPO_CONTA_REFERENCIAL_CHOICES = (
                                  ('A', 'Analítica'),
                                  ('S', 'Sintética'),
                                  )

TIPO_EMPRESA_CHOICES = (
                        ('SN', 'Simples Nacional'),
                        ('LP', 'Lucro presumido'),
                        ('LR', 'Lucro Real'),
                        )

# VALIDAÇÃO NA TABELA DE CFOP
FINANCEIRO_CFOP_CHOICES = (
                           ('S', 'Financeiro obrigatório  NF=PAGAR'),
                           ('N', 'Financeiro NÃO é obrigatório  na NF'),
                           ('B', 'NFe NÃO tem financeiro (Bonificação, etc)'),
                           ('A', 'Apenas Avisa ao usuário para decidir'),
                           )

OPERACAO_ICMS_CHOICES = (('1', 'Operação   com crédito de impostos - IPI'),
                         ('2', 'Operação   sem crédito imp - ISENTAS/NAO TRIBUTADAS - IPI'),
                         ('3', 'Operação   sem crédito imposto - OUTRAS IPI '),
                         )

OPERACAO_IPI_CHOICES = (('1', 'Operação   com crédito de impostos'),
                        ('2', 'Operação   sem crédito imp - ISENTAS/NAO TRIBUTADAS'),
                        ('3', 'Operação   sem crédito imposto - OUTRAS')
                        )

CALC_CUSTOS_CFOP_CHOICES = (('-', 'Tem Crédito - Subtrai valor do custo na nf (icm)'),
                            ('+', 'Soma valor ao preco da NF (Ex. IPI/FRETE)'),
                            ('I', 'Ignora valor, não  soma nem subtrai no custo')
                            )

FINALIDADE_CFOP_CHOICES = (
                              ('1', '1_NF-e normal'),
                              ('2', '2_NF-e complementar'),
                              ('3', '3_NF-e de ajuste'),
                              ('4', '4_NF-e Devolução/retorno'),
                           )

CALCULA_CUSTOS_CFOP_CHOICES = (('S', 'S_Calcula Custo e Custo médio nas entradas'),
                               ('N', 'N_Não calcula Custos nas entradas')
                               )

# Tipo de movimento fiscal - Vendas/Compras/bonificacao/etc - usado no BI e outros relatorios de vendas
TIPO_PRECO_CHOICES = (
                      ('V', 'V Preco VENDA tabelado no cadastro produtos'),
                      ('C', 'C Último preço de CUSTO entrada c/ cred. icms'),
                      ('E', 'E Preço com lucro zero/ponto de equlíbrio'),
                      ('N', 'N Último PREÇO de venda comprado nfe historico'),
                      ('M', 'M Preco do último CUSTO medio entrada '),
                      ('A', 'A Preco de venda Atacado do cadastro '),
                      ('P', 'P Preco a Prazo do cadastro de produtos '),
                      ('F', 'F Custo fábrica cadastro de produtos '),
                      ('I', 'I Preço indexado convertido no cadastro de prod. ')
                      )

# indPres (nfe 3.10) Indicador de presença do comprador no estabelecimento comercial no momento da operação para NFe
# Indicador de presença do comprador no estabelecimento comercial no momento da operação
# 0=Não se aplica (por exemplo, Nota Fiscal complementar ou de ajuste);
# 1=Operação presencial;
# 2=Operação não presencial, pela Internet;
# 3=Operação não presencial, Teleatendimento;
# 4=NFC-e em operação com entrega a domicílio;
# 9=Operação não presencial, outros.
INDICA_PRESENCA_CHOICES = (
                      ('0', '0=Não se aplica (por exemplo, Nota Fiscal complementar ou de ajuste'),
                      ('1', '1=Operação presencial'),
                      ('2', '2=Operação não presencial, pela Internet'),
                      ('3', '3=Operação não presencial, Teleatendimento'),
                      ('4', '4=NFC-e em operação com entrega a domicílio'),
                      ('5', '9=Operação não presencial, outros'),
                      )

# indPres (nfe 3.10) Indicador de presença do comprador no estabelecimento comercial no momento da operação PARA NFC-e
INDICA_NFCE_CHOICES = (
                      ('1', '1=Operação presencial'),
                      ('2', '2=Operação não presencial, pela Internet'),
                      ('3', '3=Operação não presencial, Teleatendimento'),
                      ('4', '4=NFC-e em operação com entrega a domicílio'),
                      ('5', '9=Operação não presencial, outros'),
                      )

# Entrega do produto na Logística - tipo de expedição
TIPO_ENTREGA_CHOICES = (
                      ('1', '1 Cliente Compra produtos e leva/Transporta da Loja'),
                      ('2', '2 Cliente pegará Produtos no Centro distribuição'),
                      ('3', '3 A Empresa Transporta e entrega os Produtos ao cliente '),
                      ('4', '4 Transporte dos produtos será terceirizado/Transportadora'),
                      ('5', '5 Empresa entrega e instala (Gera O.S. instalação'),
                      ('6', '6 Empresa irá produzir os produtos (O.P.) e entregar ao Cliente'),
                      ('7', '7 Empresa de servicos automotivos (Gera O.S. Veículos automaticos'),
                      )

# Indicador de tipo de edição de preços no pedido
ALTERA_PRECOS_CHOICES = (
                         ('S', 'S=Permite que usuario altere precos no pedido'),
                         ('N', 'N=Não permite que usuario altere preços nos pedidos'),
                         ('U', 'U=Utiliza as configuracoes do cadastro de usuários'),
                         )

# Indicador de tipo de emissao própria ou terceiros
EMISSAO_CHOICES = (
                      ('0', '0=Emissão própria'),
                      ('1', '1=Emitida por terceiros'),
                   )

# Indicador de tipo de ENTRADA / SAIDA se é transferência para filial ou outras unidades
TRANSFERENCIA_CHOICES = (('T', 'T - Transferência p/ Filial com entrada automática'),
                         ('V', 'V - Venda p/outra empresa com entrada automática'),
                         ('N', 'N - Não é transferência'),
                         )

# Indicador de tipo de frete
# Obs: A partir de 01/01/2018 passará a ser: Indicador do tipo de frete:
# 0 - Contratação do Frete por conta do Remetente (CIF)
# 1 - Contratação do Frete por conta do Destinatário (FOB)
# 2 - Contratação do Frete por conta de Terceiros
# 3 - Transporte Próprio por conta do Remetente
# 4 - Transporte Próprio por conta do Destinatário
# 9 - Sem Ocorrência de Transporte.
INDICADOR_FRETE_CHOICES = (
                           ('0', '0 - Contratação do Frete por conta do Remetente (CIF) '),
                           ('1', '1 - Contratação do Frete por conta do Destinatário (FOB) '),
                           ('2', '2 - Contratação do Frete por conta de Terceiros '),
                           ('3', '3 - Transporte Próprio por conta do Remetente '),
                           ('4', '4 - Transporte Próprio por conta do Destinatário '),
                           ('9', '9 - Sem Ocorrência de Transporte'),
                           )

# Tipo de frete - a escolher se frete for FOB
TIPO_FRETE_CHOICES = (
                      ('1', '1 - Frete Incluso no corpo da NFe COM crédito de icms'),
                      ('2', '2 - Frete Incluso no corpo da NFe SEM crédito de icms '),
                      ('3', '3 - Frete em conhecimento a parte COM crédito de icms '),
                      ('4', '4 - Frete em conhecimento a parte SEM crédito de icms '),
                      ('9', '9 - Sem Ocorrência de Transporte'),
                      )

# Status de fechamento do pedido/nfe entrada ou saida na empresa
STATUS_PEDIDO_CHOICES = (
                         ('X', 'X - Pedido em análise fiscal/financeira Saldos BLOQUEADOS'),
                         ('Y', 'Y - Pedido com saldos liberado mas ainda pendente na liberação'),
                         ('A', 'A - Pedido Aprovado/Liberado para Faturamento ou entrada'),
                         ('B', 'B - Pedido Bloqueado para faturamento '),
                         ('E', 'E - Em Análise de crédito financeiro'),
                         ('F', 'F - Faturado e Nf emitida no Caixa'),
                         ('R', 'R - Recebido cheque do cliente retorno carga Ok'),
                         ('Q', 'Q - Quitado no Financeiro todas as parcelas'),
                         ('P', 'P - Parcialmente Quitado c/ Baixas parciais'),
                         ('D', 'D - Devolvido'),
                         ('C', 'C - Cancelado'),
                         ('S', 'S - Sendo produzido Ordem de Produção'),
                         ('O', 'O - Já produzido com Ordem de Produção Fechada'),
                         ('E', 'E - Em Análise de crédito'),
                         ('T', 'T - Em trânsito para entrega'),
                         )

# Status de conferência do pedido pelos diversos setores da empresa
STATUS_CONFERENCIA_CHOICES = (
                              ('C', 'C - Conferido/liberado'),
                              ('B', 'B - Bloqueado'),
                              )


# Status de conferência dos valores na nota fiscal de entrada ou saida para ver se há diferenças 
STATUS_DIFERENCA_CHOICES = (
                             ('S', 'S para que nf esteja totalizada OK  E SEM DIFERENÇA'),
                             ('D', 'D para NF com diferença e com saldo não atualizado'),
                           )

# Indicador do tipo de pagamento no sped e na contabilidade 0- À vista 1- A prazo 9- Sem pagamento
TIPO_PAGAMENTO_CHOICES = (
                          ('0', '0- À vista'),
                          ('1', '1- A prazo'),
                          ('9', '9- Sem pagamento'),
                          )


# Indicador do tipo de DOCUMENTOS NO FINANCEIRO
TIPO_DOCUMENTO_CHOICES = (
                          ('01', '01 = Dinheiro'),
                          ('02', '02 = Cheque'),
                          ('03', '03 = Cartão de Crédito'),
                          ('04', '04 = Cartão de Débito"'),
                          ('05', '05 = Crédito Loja)'),
                          ('11', '11 = Vale Refeição'),
                          ('12', '12 = Vale Presente'),
                          ('13', '13 = Vale Combustível'),
                          ('99', '99 = Outros'),
                          )

# Modalidade  do icms 1=trib 2=Isento ou não  trib 3=
MODALIDADE_ICMS_CHOICES = (
                          ('1', '1 Tributado'),
                          ('2', '2 Isento ou não tributado'),
                          ('3', '3 Outros'),
                          )

# Modalidade  do icms 1=trib 2=Isento ou não  trib 3=
MODALIDADE_IPI_CHOICES = (
                          ('1', '1 Tributado'),
                          ('2', '2 Isento ou não tributado'),
                          ('3', '3 Outros'),
                          )

# Modalidade da base de calculo do icms
MODALIDADE_CALC_ICMS_CHOICES = (
                                ('3', '3 valor da operação'),
                                ('0', '0 Margem de Valor Agregado(%)'),
                                ('1', '1 Pauta fiscal (Valor)'),
                                ('2', '2 Preço Tabelado Máximo valor'),
                               )


# Modalidade da base de cálculo do icms substituição tributária
MODALIDADE_ICMSSUB_CHOICES = (
                              ('4', '4 Margem Valor Agregado (%)'),
                              ('0', '0 Preço tab ou máximo sugerido'),
                              ('1', '1 Lista Negativa (valor)'),
                              ('2', '2 Lista Positiva (valor) '),
                              ('3', '3 Lista Neutra (valor) '),
                              ('5', '5 Pauta (valor) '),
                              )

# Status do registro de venda - repete no pedido
STATUS_PEDIDO_ITEM_CHOICES = (('0', 'Orçamentos (não gera PedidoItensNf (subserie ORC)'),
                              ('C', 'Cancelado (deleta PedidoItensNf '),
                              ('D', 'Devolução de cliente/fornecedor Subserie (DEV) '),
                              ('E', 'Encomenda para entrega futura '),
                              ('B', 'Pedido Bloqueado para análise'),
                              ('E', 'Em Análise de crédito '),
                              ('A', 'Aprovado para faturamento  '),
                              ('F', 'Faturado e Nf emitida no Caixa  '),
                              ('R', 'Recebido cheque do cliente  '),
                              ('Q', 'Quitado no Financeiro ok  '),
                              ('P', 'Parcialmente Quitado  '),
                              ('S', 'Sendo produzido Ordem Produção'),
                              ('T', 'Pedido em trânsito'),
                              ('r', 'Pedido Web recepcionado pelo Sistema Usesoft'),
                              ('W', 'Pedido Web gravado'),
                              )

INDICADOR_PAGAMENTO_CHOICES = (
                              ('0', 'Pagamento `vista na NFe'),
                              ('1', 'Pagamento a Prazo na Nfe'),
                              ('2', 'Outros pagamentos na NFe'),
                              )

# Código de Regime Tributário
REGIME_TRIBUTARIO_CHOICES = (
                             ('1', '1=Simples Nacional'),
                             ('1', '2=Simples Nacional, excesso sublimite de receita bruta'),
                             ('3', '3=Regime Normal. (v2.0).'),
                              )

# Código de Regime Tributário
MULTIPLICA_DIVIDE_CHOICES = (
                             ('X', 'Multiplica pela quantidade na entrada'),
                             ('/', 'Divide pela quantidade na entrada'),
                            )

# Modalidade  de  determinação da BC da pauta fiscal
MODALIDADE_PAUTA_CHOICES = (
    ('0', '0 - Valor mínimo a ser considerado (se valor da venda for maior assume valor venda)'),
    ('1', '1 - Valor fixo de pauta independente da venda')
                             )


# Este campo será preenchido quando o campo anterior estiver preenchido. Informar o motivo da desoneração:
MOTIVO_DESONERACAO_ICM_CHOICES = (
                                  ('0', '1  Táxi )'),
                                  ('1', '2  Deficiente Físico '),
                                  ('1', '3  Produtor Agropecuário '),
                                  ('1', '4  Frotista/Locadora  '),
                                  ('1', '5  Diplomático/Consular '),
                                  ('1', '6  Utilitários e Motocicletas da Amazônia Ocidental e Áreas de Livre Comércio'
                                        ' (Resolução 714/88 e 790/94  CONTRAN e suas alterações)  '),
                                  ('1', '7  SUFRAMA'),
                                  ('1', '9  outros '),
                                  )


TIPO_CODIGO_CHOICES = (
                       ('0', 'GS1/GTIN Ean 8-12-13-14'),
                       ('1', 'Código alternativo'),
                       ('2', 'Referência de fábrica'),
                       ('3', 'Código anterior deste produto'),
                       ('4', 'Código Exceção NCM(TIPI)SPED'),
                       ('5', 'Cod TAB ANP combustíveis'),
                       )


ESCOLHE_DESCONTO_CHOICES = (
                        ('M', 'Mostrar % de desconto na tela e no pedido'),
                        ('L', 'Mostra somente valor líquido após Descontos'),
                       )


def quantidade_maior_que_zero(value):
    if value <= 0:
        raise ValidationError(
            'A quantidade informada tem que ser MAIOR QUE ZERO',
            params={'value': value},
        )