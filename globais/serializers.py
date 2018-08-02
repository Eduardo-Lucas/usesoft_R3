from rest_framework import serializers

from globais.models import Cfop, MensagemPadrao, Municipio, Uf, PaisIbge, TipoOperacaoFiscal, CodigoNcm


class CfopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cfop
        fields = ['url', 'id', 'codigo', 'descricao', 'tipomovimentofiscal', 'natureza_base_calc_cred_pis',
                  'mensagempadrao',
                  'dias_devolucao', 'pode_subst_tributaria', 'tributado_icms', 'credito_icms', 'reduz_base_icms',
                  'operacao_icms', 'tributado_ipi', 'credito_ipi', 'operacao_ipi', 'tributado_pis_cofins',
                  'credito_pis_cofins', 'cfop_padrao', 'movimenta_estoques', 'movimenta_financeiro', 'calcula_custos',
                  'custo_icms', 'custo_ipi', 'custo_frete', 'custo_icms_frete', 'custo_pis', 'custo_cofins',
                  'custo_seguro', 'custo_despesas', 'custo_descontos', 'custo_icms_sub', 'custo_antecipacao_trib',
                  'finalidade_nfe', 'doc_referenciado',
                  ]


class MensagemPadraoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MensagemPadrao
        fields = ['codigo', 'descricao', 'habilitado', ]


class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'


class UfSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Uf
        fields = '__all__'


class PaisIbgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaisIbge
        fields = '__all__'


class TipoOperacaoFiscalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoOperacaoFiscal
        fields = '__all__'


class CodigoNcmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CodigoNcm
        fields = '__all__'
