from rest_framework import serializers

from materiais.models import PedidoWeb, PedidoWebItem, Produto


class PedidoWebSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PedidoWeb
        fields = ('url', 'id', 'serie', 'subserie', 'indicador_pagamento_nfe', 'status_pedido', 'regime_tributario',
                  'notafiscal', 'autorizacao_faturamento', 'autorizacao_numitem', 'indicador_emitente',
                  'situacaodocumentosped', 'modelodocumentofiscal', 'data_pedido', 'data_emissao', 'data_saida',
                  'data_movimento', 'created', 'updated', 'cfop', 'tipo_de_pagamento', 'prazo_de_pagamento',
                  'participante', 'vendedor', 'mensagempadrao',
                  'tipo_pedido', 'indicador_presenca_nfe', 'tipo_preco_pedido', 'total_produtos', 'perc_desc',
                  'base_calc_ipi', 'valor_ipi', 'perc_ipi', 'valor_contabil', 'base_calc_icms', 'valor_icms',
                  'perc_icms', 'base_calc_icms_sub', 'valor_icms_sub', 'valor_despesas_acess', 'base_calc_pis',
                  'valor_pis', 'base_calc_cofins', 'valor_cofins', 'valor_seguro', 'base_calc_issqn', 'perc_issqn',
                  'quantidade_servicos', 'valor_servicos', 'transportadora', 'valor_frete', 'valor_icm_frete',
                  'cif_fob_frete', 'tipo_frete', 'status_manifestacao', 'status_contabilidade', 'status_financeiro',
                  'status_precos', 'status_expedicao', 'status_diferenca',  )


class PedidoWebItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PedidoWebItem
        fields = ['url', 'pedidoweb', 'sequencia', 'produto', 'unidade', 'descricao', 'observacoes', 'cfop',
                  'codigo_ncm',
                  'codigo_cest', 'status_pedido_item', 'autorizacao_faturamento', 'autorizacao_numitem', 'quantidade',
                  'peso_liquido', 'peso_bruto', 'metro_cubico', 'movimenta_estoques', 'saldo_fisico', 'saldo_fiscal',
                  'preco_custo', 'preco_medio', 'preco_custo_nfe', 'preco_medio_nfe', 'preco_unitario', 'perc_desc',
                  'custo_informado', 'participante', 'total_produto', 'modalidade_ipi', 'situacao_tributaria_ipi',
                  'base_calc_ipi', 'perc_ipi', 'perc_red_ipi', 'modalidade_calculo', 'modalidade_icms',
                  'situacao_tributaria_icms', 'base_calc_icms', 'perc_icms', 'perc_antec_tributaria', 'perc_red_icms',
                  'modalidade_calculo_subst', 'base_calc_icms_sub', 'perc_mva_sub', 'perc_icms_sub',
                  'perc_reducao_icms_sub', 'base_calc_antecipacao_trib', 'perc_antecipacao_trib',
                  'situacao_tributaria_pis', 'base_calc_pis', 'perc_pis', 'situacao_tributaria_cofins',
                  'base_calc_cofins', 'perc_fundo_pobreza', 'perc_trib_aproximado', 'base_calc_import', 'perc_import',
                  'base_calc_issqn', 'perc_issqn', 'perc_desp_acessorias', 'perc_seguro', 'perc_frete',
                  'natureza_custos', 'centro_custo', 'codigo_promocao']


class ProdutoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Produto
        fields = '__all__'







