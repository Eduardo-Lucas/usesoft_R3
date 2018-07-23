from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from financeiro.models import NaturezaCusto, TipoPagamento, TipoDocumento, PrazoPagamento, CentroCusto

# admin.site.register(TipoPagamento)
from globais.models import ModeloDocumentoFiscal

admin.site.register(NaturezaCusto)
admin.site.register(CentroCusto)


@admin.register(TipoDocumento)
class TipoDocumentoResource(ImportExportModelAdmin):
    pass


@admin.register(TipoPagamento)
class TipoPagamentoResource(ImportExportModelAdmin):
    pass


@admin.register(PrazoPagamento)
class PrazoPagamentoResource(ImportExportModelAdmin):
    pass
