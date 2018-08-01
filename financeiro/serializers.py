from rest_framework import serializers

from financeiro.models import TipoPagamento, PrazoPagamento, TipoDocumento


class TipoPagamentoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TipoPagamento
        fields = ['codigo', 'descricao', 'habilitado', 'negociada', 'venda_parcelada', 'imprime_na_nfe',
                  'habilitado_web', 'num_parcelas', 'prazos_padroes', 'prazo_maximo', 'tipo_documento', 'valor_minimo',
                  'valor_maximo', ]


class PrazoPagamentoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PrazoPagamento
        fields = ['codigo', 'descricao', ]


class TipoDocumentoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TipoDocumento
        fields = '__all__'


