from rest_framework import viewsets

from globais.models import Cfop, MensagemPadrao, Municipio, Uf, PaisIbge, TipoOperacaoFiscal
from globais.serializers import CfopSerializer, MensagemPadraoSerializer, MunicipioSerializer, UfSerializer, \
    PaisIbgeSerializer, TipoOperacaoFiscalSerializer


class CfopViewSet(viewsets.ModelViewSet):
    """
    Lista todos os CFOPs, ou cria um novo CFOP.
    """
    queryset = Cfop.objects.all()
    serializer_class = CfopSerializer


class MensagemPadraoViewSet(viewsets.ModelViewSet):
    """
    Lista todos as Mensagens Padrões, ou cria uma nova.
    """
    queryset = MensagemPadrao.objects.all()
    serializer_class = MensagemPadraoSerializer


class MunicipioViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Municípios, ou cria um novo.
    """
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer


class UfViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Unidades Federativas, ou cria uma nova.
    """
    queryset = Uf.objects.all()
    serializer_class = UfSerializer


class PaisIbgeViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Unidades Federativas, ou cria uma nova.
    """
    queryset = PaisIbge.objects.all()
    serializer_class = PaisIbgeSerializer


class TipoOperacaoFiscalViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Tipos de Operações Fiscais , ou cria uma nova.
    """
    queryset = TipoOperacaoFiscal.objects.all()
    serializer_class = TipoOperacaoFiscalSerializer


