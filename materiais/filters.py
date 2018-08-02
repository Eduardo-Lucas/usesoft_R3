from materiais.models import PedidoWeb, Produto

from django_filters import rest_framework as filters


class PedidoWebFilter(filters.FilterSet):
    ano_pedido = filters.NumberFilter(name='data_pedido', lookup_expr='year')
    ano_pedido__gt = filters.NumberFilter(name='data_pedido', lookup_expr='year__gt')
    ano_pedido__lt = filters.NumberFilter(name='data_pedido', lookup_expr='year__lt')
    mes_pedido = filters.NumberFilter(name='data_pedido', lookup_expr='month')
    total_produtos = filters.NumberFilter()
    total_produtos__gt = filters.NumberFilter(field_name='total_produtos', lookup_expr='gt')
    total_produtos__lt = filters.NumberFilter(field_name='total_produtos', lookup_expr='lt')

    class Meta:
        model = PedidoWeb
        fields = ['ano_pedido', 'ano_pedido__gt', 'mes_pedido', 'participante', 'tipo_de_pagamento',
                  'prazo_de_pagamento', 'total_produtos', 'total_produtos__gt', 'total_produtos__lt',
                  'vendedor', ]


class ProdutoFilter(filters.FilterSet):
    min_preco_venda = filters.NumberFilter(field_name="preco_venda", lookup_expr='gte')
    max_preco_venda = filters.NumberFilter(field_name="preco_venda", lookup_expr='lte')

    class Meta:
        model = Produto
        fields = ['categoria', 'disponivel', 'min_preco_venda', 'max_preco_venda', ]
