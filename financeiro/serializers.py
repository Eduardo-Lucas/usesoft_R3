from rest_framework import serializers

from financeiro.models import TipoPagamento


class TipoPagamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoPagamento
        fields = '__all__'
