from rest_framework import serializers

from materiais.models import PedidoWeb, PedidoWebItem


class PedidoWebSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.HyperlinkedRelatedField(many=True, view_name='pedidowebitem-detail', read_only=True)

    class Meta:
        model = PedidoWeb
        fields = ('serie', 'subserie', 'indicador_pagamento_nfe', 'status_pedido', 'regime_tributario', 'notafiscal',
                  'autorizacao_faturamento', 'autorizacao_numitem', 'indicador_emitente', 'situacaodocumentosped',
                  'modelodocumentofiscal', 'data_pedido', 'data_emissao', 'data_saida', 'data_movimento', 'created',
                  'updated', 'cfop', 'tipo_de_pagamento', 'prazo_de_pagamento', 'participante', 'vendedor',
                  'mensagempadrao',
                  'tipo_pedido', 'indicador_presenca_nfe', 'tipo_preco_pedido', 'total_produtos', 'perc_desc',
                  'base_calc_ipi', 'valor_ipi', 'perc_ipi', 'valor_contabil', 'base_calc_icms', 'valor_icms',
                  'perc_icms', 'base_calc_icms_sub', 'valor_icms_sub', 'valor_despesas_acess', 'base_calc_pis',
                  'valor_pis', 'base_calc_cofins', 'valor_cofins', 'valor_seguro', 'base_calc_issqn', 'perc_issqn',
                  'quantidade_servicos', 'valor_servicos', 'transportadora', 'valor_frete', 'valor_icm_frete',
                  'cif_fob_frete', 'tipo_frete', 'status_manifestacao', 'status_contabilidade', 'status_financeiro',
                  'status_precos', 'status_expedicao', 'status_diferenca', 'items', )


class PedidoWebItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PedidoWebItem
        fields = '__all__'

