from materiais.models import PedidoWeb, PedidoWebItem
from materiais.serializers import PedidoWebSerializer, PedidoWebItemSerializer

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


class PedidoWebItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PedidoWeb to be viewed or edited.
    """
    queryset = PedidoWebItem.objects.all().order_by('sequencia')
    serializer_class = PedidoWebItemSerializer
