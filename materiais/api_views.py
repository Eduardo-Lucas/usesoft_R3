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
    queryset = PedidoWeb.objects.all().order_by('-id')[:100]
    serializer_class = PedidoWebSerializer


class PedidoWebItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PedidoWebItem to be viewed or edited.
    """
    queryset = PedidoWebItem.objects.all().order_by('sequencia')
    serializer_class = PedidoWebItemSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Produto be viewed or edited.
    """
    queryset = Produto.objects.all().order_by('descricao')[:100]
    serializer_class = ProdutoSerializer
