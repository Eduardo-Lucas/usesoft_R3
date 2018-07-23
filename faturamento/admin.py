from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from faturamento.models import GrupoParticipante, Participante, RegiaoDeVenda


@admin.register(GrupoParticipante)
class ParticipanteAdmin(ImportExportModelAdmin):
    pass


@admin.register(RegiaoDeVenda)
class ParticipanteAdmin(ImportExportModelAdmin):
    pass


@admin.register(Participante)
class ParticipanteAdmin(ImportExportModelAdmin):
    pass
