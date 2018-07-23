from materiais.models import PedidoWeb
from materiais.serializers import PedidoWebSerializer

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
