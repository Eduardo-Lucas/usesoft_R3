from django_filters.rest_framework import DjangoFilterBackend

from materiais.models import PedidoWeb, PedidoWebItem, Produto
from materiais.serializers import PedidoWebSerializer, PedidoWebItemSerializer, ProdutoSerializer

from rest_framework import viewsets

"""
    API views 
"""


class PedidoWebViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PedidoWeb to be viewed or edited.
    """
    queryset = PedidoWeb.objects.all().order_by('-id')
    serializer_class = PedidoWebSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status_pedido', 'participante', 'tipo_de_pagamento', 'prazo_de_pagamento')


class PedidoWebItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PedidoWebItem to be viewed or edited.
    """
    queryset = PedidoWebItem.objects.all().order_by('sequencia')
    serializer_class = PedidoWebItemSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('pedidoweb', 'produto', 'descricao')


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Produto be viewed or edited.
    """
    queryset = Produto.objects.all().order_by('descricao')
    serializer_class = ProdutoSerializer
