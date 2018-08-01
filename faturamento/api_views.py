from rest_framework import generics, viewsets

from faturamento.models import Participante, RegiaoDeVenda, GrupoParticipante
from faturamento.serializers import ParticipanteSerializer, RegiaoDeVendaSerializer, GrupoParticipanteSerializer


class ParticipanteViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Participantes, ou cria um novo Participante.
    """
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer


class RegiaoDeVendaViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Regiões de Venda, ou cria uma nova Região de Venda.
    """
    queryset = RegiaoDeVenda.objects.all()
    serializer_class = RegiaoDeVendaSerializer


class GrupoParticipanteViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Regiões de Venda, ou cria uma nova Região de Venda.
    """
    queryset = GrupoParticipante.objects.all()
    serializer_class = GrupoParticipanteSerializer




