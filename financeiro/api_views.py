from rest_framework import generics, viewsets

from financeiro.models import TipoPagamento, PrazoPagamento, TipoDocumento
from financeiro.serializers import TipoPagamentoSerializer, PrazoPagamentoSerializer, TipoDocumentoSerializer


class TipoPagamentoViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Tipo de Pagamento, ou cria um novo Tipo de Pagamento.
    """
    queryset = TipoPagamento.objects.all()
    serializer_class = TipoPagamentoSerializer


class PrazoPagamentoViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Tipo de Pagamento, ou cria um novo Tipo de Pagamento.
    """
    queryset = PrazoPagamento.objects.all()
    serializer_class = PrazoPagamentoSerializer


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Tipo de Pagamento, ou cria um novo Tipo de Pagamento.
    """
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer

