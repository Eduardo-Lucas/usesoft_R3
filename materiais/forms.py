from django import forms
from django.forms import inlineformset_factory, ModelForm

from materiais.models import PedidoWeb, PedidoWebItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = PedidoWeb
        fields = ['vendedor', 'participante', 'tipo_de_pagamento', 'prazo_de_pagamento', 'observacoes']


class PedidoWebForm(forms.ModelForm):
    class Meta:
        model = PedidoWeb
        fields = ['vendedor', 'participante', 'vendedor', 'tipo_de_pagamento', 'prazo_de_pagamento']
        exclude = ['observacoes']


class PedidoWebItemForm(forms.ModelForm):
    class Meta:
        model = PedidoWebItem
        fields = ['produto', 'quantidade', 'preco_unitario', 'perc_desc', 'total_produto']
        exclude = ['sequencia', 'unidade', 'descricao', 'observacoes', 'cfop', 'codigo_ncm', 'codigo_cest',
                   'status_pedido_item', 'autorizacao_faturamento', 'autorizacao_numitem', 'peso_liquido', 'peso_bruto',
                   'metro_cubico', 'movimenta_estoques', 'saldo_fisico', 'saldo_fiscal', 'preco_custo', 'preco_medio',
                   'preco_custo_nfe', 'preco_medio_nfe', 'custo_informado', 'data_movimento',
                   'participante', 'modalidade_ipi', 'situacao_tributaria_ipi', 'base_calc_ipi',
                   'perc_ipi', 'perc_red_ipi', 'modalidade_calculo', 'modalidade_icms', 'situacao_tributaria_icms',
                   'base_calc_icms', 'perc_icms', 'perc_antec_tributaria', 'perc_red_icms', 'modalidade_calculo_subst',
                   'perc_mva_sub', 'perc_icms_sub', 'perc_reducao_icms_sub', 'base_calc_antecipacao_trib',
                   'perc_antecipacao_trib', 'situacao_tributaria_pis', 'base_calc_pis', 'perc_pis',
                   'situacao_tributaria_cofins', 'base_calc_cofins', 'perc_fundo_pobreza', 'perc_trib_aproximado',
                   'base_calc_import', 'perc_import', 'base_calc_issqn', 'perc_issqn', 'perc_desp_acessorias',
                   'perc_seguro', 'perc_frete', 'natureza_custos', 'centro_custo', 'codigo_promocao']


PedidoWebFormSet = inlineformset_factory(PedidoWeb, PedidoWebItem,
                                         form=PedidoWebItemForm,
                                         fields=('produto', 'quantidade', 'preco_unitario', 'perc_desc',
                                                 'total_produto'),
                                         can_delete=False,
                                         extra=2,
                                         validate_min=False)
