from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from faturamento.models import RegiaoDeVenda
from .models import Uf, Municipio, PaisIbge, CodigoNcm, ModeloDocumentoFiscal, SituacaoDocumentoSped, Cfop, \
    TipoOperacaoFiscal, CodigoCest, SituacaoTribIpi, SituacaoTribIcms, SituacaoTribPis, SituacaoTribCofins, \
    MensagemPadrao


class UfResource(resources.ModelResource):
    class Meta:
        model = Uf
        fields = ('id', 'codigo', 'sigla_estado', 'estado', 'data_publicacao')


class MunicipioResource(resources.ModelResource):
    class Meta:
        model = Municipio
        fields = ('codigo', 'descricao', 'data_publicacao', 'id')


class PaisIbgeResource(resources.ModelResource):
    class Meta:
        model = PaisIbge
        fields = ('codigo', 'descricao', 'data_publicacao', 'id')


class CodigoNcmResource(resources.ModelResource):
    class Meta:
        model = CodigoNcm
        fields = ('codigo', 'unidade', 'data_publicacao', 'descricao_unidade', 'id')


class ModeloDocumentoFiscalResource(resources.ModelResource):
    class Meta:
        model = ModeloDocumentoFiscal
        fields = '__all__'


class SituacaoDocumentoSpedResource(resources.ModelResource):
    class Meta:
        model = SituacaoDocumentoSped
        fields = '__all__'


class CodigoCestResource(resources.ModelResource):
    class Meta:
        model = CodigoCest
        fields = '__all__'


class CfopResource(resources.ModelResource):
    tipomovimentofiscal = fields.Field(
        column_name='tipomovimentofiscal',
        attribute='tipomovimentofiscal',
        widget=ForeignKeyWidget(TipoOperacaoFiscal, 'pk'))

    class Meta:
        model = Cfop
        fields = '__all__'


class TipoOperacaoFiscalResource(resources.ModelResource):
    class Meta:
        model = TipoOperacaoFiscal
        fields = '__all__'


class RegiaoDeVendaResource(resources.ModelResource):
    class Meta:
        model = RegiaoDeVenda
        fields = '__all__'


class SituacaoTribIpiResource(resources.ModelResource):
    class Meta:
        model = SituacaoTribIpi
        fields = '__all__'


class SituacaoTribIcmsResource(resources.ModelResource):
    class Meta:
        model = SituacaoTribIcms
        fields = '__all__'


class SituacaoTribPisResource(resources.ModelResource):
    class Meta:
        model = SituacaoTribPis
        fields = '__all__'


class SituacaoTribCofinsResource(resources.ModelResource):
    class Meta:
        model = SituacaoTribCofins
        fields = '__all__'


class MensagemPadraoResource(resources.ModelResource):
    class Meta:
        model = MensagemPadrao
        fields = '__all__'
