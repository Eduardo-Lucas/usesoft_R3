from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from materiais.models import Produto, Categoria, PedidoWebItem, PedidoWeb, ProdutoPromocao, ProdutoDepartamento, \
    ProdutoTributacao, PedidoTipo


class ProdutoInLine(admin.TabularInline):
    model = Produto
    extra = 0


class CategoriaAdmin(admin.ModelAdmin):
    inlines = [
        ProdutoInLine,
    ]

    class Meta:
        model = Categoria


class OrderItemInline(admin.TabularInline):
    model = PedidoWebItem
    raw_id_fields = ['produto']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'participante', 'tipo_de_pagamento', 'prazo_de_pagamento']
    list_filter = ['participante', 'tipo_de_pagamento', 'prazo_de_pagamento', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(PedidoWeb, OrderAdmin)
admin.site.register(ProdutoDepartamento)


@admin.register(Categoria)
class CategoriaResource(ImportExportModelAdmin):
    pass


@admin.register(Produto)
class ProdutoResource(ImportExportModelAdmin):
    pass


@admin.register(ProdutoTributacao)
class ProdutoTributacaoResource(ImportExportModelAdmin):
    pass


@admin.register(ProdutoPromocao)
class ProdutoPromocaoResource(ImportExportModelAdmin):
    pass


@admin.register(PedidoTipo)
class PedidoTipoResource(ImportExportModelAdmin):
    pass
