from rest_framework import serializers

from faturamento.models import Participante, RegiaoDeVenda, GrupoParticipante


class ParticipanteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Participante
        fields = ['url', 'id', 'razao_social', 'nome_fantasia', 'fisica_juridica', 'cnpj_cpf', 'inscricao_estadual',
                  'inscricao_municipal', 'codigo', 'regiao_de_venda', 'grupo', 'endereco', 'complemento', 'numero',
                  'bairro', 'cidade', 'cep', 'estado', 'pais', 'telefone', 'telefone2', 'celular', 'celular2', 'email',
                   ]


class RegiaoDeVendaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RegiaoDeVenda
        fields = ['url', 'codigo', 'descricao', 'habilitado', ]


class GrupoParticipanteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GrupoParticipante
        fields = ['url', 'codigo', 'descricao', 'habilitado', ]

