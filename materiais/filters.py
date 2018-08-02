from materiais.models import PedidoWeb, Produto
import django_filters


class PedidoWebFilter(django_filters.FilterSet):
    ano_pedido = django_filters.NumberFilter(name='data_pedido', lookup_expr='year')
    ano_pedido__gt = django_filters.NumberFilter(name='data_pedido', lookup_expr='year__gt')
    ano_pedido__lt = django_filters.NumberFilter(name='data_pedido', lookup_expr='year__lt')
    mes_pedido = django_filters.NumberFilter(name='data_pedido', lookup_expr='month')
    total_produtos = django_filters.NumberFilter()
    total_produtos__gt = django_filters.NumberFilter(field_name='total_produtos', lookup_expr='gt')
    total_produtos__lt = django_filters.NumberFilter(field_name='total_produtos', lookup_expr='lt')

    class Meta:
        model = PedidoWeb
        fields = ['ano_pedido', 'ano_pedido__gt', 'mes_pedido', 'participante', 'tipo_de_pagamento',
                  'prazo_de_pagamento', 'total_produtos', 'total_produtos__gt', 'total_produtos__lt',
                  'vendedor', ]


class ProdutoFilter(django_filters.FilterSet):
    class Meta:
        model = Produto
        fields = {
            'preco_venda': ['icontains', ],
            'produto': ['icontains', ],
        }
