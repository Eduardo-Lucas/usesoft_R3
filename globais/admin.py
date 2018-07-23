from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from globais.models import SituacaoTribIpi, SituacaoTribIcms, SituacaoTribPis, SituacaoTribCofins, Uf, Municipio, \
    PaisIbge, Cfop, ModeloDocumentoFiscal, SituacaoDocumentoSped, TipoOperacaoFiscal, MensagemPadrao, \
    CodigoNcm, CodigoCest


@admin.register(Uf)
class UfAdmin(ImportExportModelAdmin):
    pass


@admin.register(Cfop)
class CfopAdmin(ImportExportModelAdmin):
    pass


@admin.register(Municipio)
class MunicipioAdmin(ImportExportModelAdmin):
    pass


@admin.register(PaisIbge)
class PaisIbgeAdmin(ImportExportModelAdmin):
    pass


@admin.register(CodigoNcm)
class CodigoNcmAdmin(ImportExportModelAdmin):
    pass


@admin.register(CodigoCest)
class CodigoCestAdmin(ImportExportModelAdmin):
    pass


@admin.register(ModeloDocumentoFiscal)
class ModeloDocumentoFiscalResource(ImportExportModelAdmin):
    pass


@admin.register(SituacaoDocumentoSped)
class SituacaoDocumentoSpedResource(ImportExportModelAdmin):
    pass


@admin.register(TipoOperacaoFiscal)
class TipoOperacaoFiscalResource(ImportExportModelAdmin):
    pass


@admin.register(SituacaoTribIpi)
class SituacaoTribIpiResource(ImportExportModelAdmin):
    pass


@admin.register(SituacaoTribIcms)
class SituacaoTribIcmsResource(ImportExportModelAdmin):
    pass


@admin.register(SituacaoTribPis)
class SituacaoTribPisResource(ImportExportModelAdmin):
    pass


@admin.register(SituacaoTribCofins)
class SituacaoTribCofinsResource(ImportExportModelAdmin):
    pass


@admin.register(MensagemPadrao)
class MensagemPadraoResource(ImportExportModelAdmin):
    pass



