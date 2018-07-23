from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from globais.models import CodigoNcm, TipoOperacaoFiscal, Uf, SituacaoTribIcms, SituacaoTribPis
from .models import Produto, Categoria, ProdutoTributacao, PedidoTipo, ProdutoPromocao


class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProdutoResource(resources.ModelResource):
    categoria = fields.Field(
        column_name='categoria',
        attribute='categoria',
        widget=ForeignKeyWidget(Categoria, 'pk'))

    codigo_ncm = fields.Field(
        column_name='codigo_ncm',
        attribute='codigo_ncm',
        widget=ForeignKeyWidget(CodigoNcm, 'pk'))

    class Meta:
        model = Produto
        fields = ('categoria', 'disponivel', 'produto', 'descricao', 'slug', 'image', 'aplicacao', 'unidade',
                  'num_decimais', 'tributacao_produto', 'codigo_ncm', 'codigo_cest', 'codigo_nbs', 'fabricante',
                  'grupo', 'departamento', 'preco_venda', 'saldo_negativo', 'saldo_fiscal_negativo',
                  'localizacao_deposito', 'embalagem_venda', 'embalagem_compra', 'quantidade_por_embalagem',
                  'multiplica_divide', 'peso_liquido', 'peso_bruto', 'largura', 'altura', 'comprimento',
                  'largura_palet', 'altura_palet', 'comprimento_palet', 'peso_liquido_palet', 'peso_bruto_palet',
                  'quantidade_produtos_palet', 'codigo_cor', 'codigo_tamanho', 'codigo_densidade', 'id')


class ProdutoTributacaoResource(resources.ModelResource):
    estado = fields.Field(
        column_name='estado',
        attribute='estado',
        widget=ForeignKeyWidget(Uf, 'pk'))

    tipooperacaofiscal = fields.Field(
        column_name='tipooperacaofiscal',
        attribute='tipooperacaofiscal',
        widget=ForeignKeyWidget(TipoOperacaoFiscal, 'pk'))

    situacao_tributaria_icms = fields.Field(
        column_name='situacao_tributaria_icms',
        attribute='situacao_tributaria_icms',
        widget=ForeignKeyWidget(SituacaoTribIcms, 'pk'))

    situacao_tributaria_pis = fields.Field(
        column_name='situacao_tributaria_pis',
        attribute='situacao_tributaria_pis',
        widget=ForeignKeyWidget(SituacaoTribPis, 'pk'))

    class Meta:
        model = ProdutoTributacao
        fields = '__all__'


class ProdutoPromocaoResource(resources.ModelResource):
    class Meta:
        model = ProdutoPromocao
        fields = '__all__'


class PedidoTipoResource(resources.ModelResource):
    tipooperacaofiscal = fields.Field(
        column_name='tipooperacaofiscal',
        attribute='tipooperacaofiscal',
        widget=ForeignKeyWidget(TipoOperacaoFiscal, 'codigo'))

    class Meta:
        model = PedidoTipo
        fields = '__all__'

