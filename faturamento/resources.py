from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from globais.models import Uf, Municipio, PaisIbge
from .models import Participante, GrupoParticipante, RegiaoDeVenda


class GrupoParticipanteResource(resources.ModelResource):
    class Meta:
        model = GrupoParticipante
        fields = '__all__'


class RegiaoDeVendaResource(resources.ModelResource):
    class Meta:
        model = RegiaoDeVenda
        fields = '__all__'


class ParticipanteResource(resources.ModelResource):
    regiao_de_venda = fields.Field(column_name='regiao_de_venda',
                                   attribute='regiao_de_venda',
                                   widget=ForeignKeyWidget(RegiaoDeVenda, 'pk'))

    grupo = fields.Field(column_name='grupo',
                         attribute='grupo',
                         widget=ForeignKeyWidget(GrupoParticipante, 'pk'))

    cidade = fields.Field(column_name='cidade',
                          attribute='cidade',
                          widget=ForeignKeyWidget(Municipio, 'pk'))

    estado = fields.Field(column_name='estado',
                          attribute='estado',
                          widget=ForeignKeyWidget(Uf, 'pk'))

    pais = fields.Field(column_name='pais',
                        attribute='pais',
                        widget=ForeignKeyWidget(PaisIbge, 'pk'))

    class Meta:
        model = Participante
        fields = '__all__'
