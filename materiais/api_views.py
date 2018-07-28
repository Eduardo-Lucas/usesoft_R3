from materiais.models import PedidoWeb, PedidoWebItem
from materiais.serializers import PedidoWebSerializer, PedidoWebItemSerializer

from rest_framework import generics

"""
    API views 
"""


class PedidoWebList(generics.ListCreateAPIView):
    """
    Lista todos os PedidoWeb, ou cria um novo PedidoWeb.
    """
    queryset = PedidoWeb.objects.all()
    serializer_class = PedidoWebSerializer


class PedidoWebDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, atualiza ou apaga uma instância de PedidoWeb.
    """
    queryset = PedidoWeb.objects.all()
    serializer_class = PedidoWebSerializer


class PedidoWebItemList(generics.ListCreateAPIView):
    """
    Lista todos os PedidoWebItem, ou cria um novo PedidoWebItem.
    """
    queryset = PedidoWebItem.objects.all()
    serializer_class = PedidoWebItemSerializer


class PedidoWebItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Recupera, atualiza ou apaga uma instância de PedidoWeb.
    """
    queryset = PedidoWebItem.objects.all()
    serializer_class = PedidoWebItemSerializer


