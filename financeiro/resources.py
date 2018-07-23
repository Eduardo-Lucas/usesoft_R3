from import_export import resources, fields

from financeiro.models import TipoPagamento, PrazoPagamento, TipoDocumento


class TipoDocumentoResource(resources.ModelResource):
    class Meta:
        model = TipoDocumento
        fields = '__all__'


class TipoPagamentoResource(resources.ModelResource):
    class Meta:
        model = TipoPagamento
        fields = '__all__'


class PrazoPagamentoResource(resources.ModelResource):
    class Meta:
        model = PrazoPagamento
        fields = '__all__'


