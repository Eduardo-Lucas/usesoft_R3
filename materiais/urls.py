from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from materiais import views, api_views
from materiais.views import PedidoWebTradicionalList, PedidoWebTradicionalDetalhe, PedidoWebTradicionalCreate, \
    PedidoWebTradicionalUpdate, ProdutoDetalhe

app_name = 'materiais'

urlpatterns = [

    # Pedido Tipo: Tradicional
    url(r'^pedidoweb_list/$', PedidoWebTradicionalList.as_view(), name='pedidoweb_list'),
    url(r'^pedidoweb_list/(?P<pk>[0-9]+)/$', PedidoWebTradicionalDetalhe.as_view(), name="pedidoweb_detail"),
    url(r'^pedidoweb_add/$', PedidoWebTradicionalCreate.as_view(), name='pedidoweb_add'),
    url(r'^pedidoweb_edit/(?P<pk>[0-9]+)/edit/$', PedidoWebTradicionalUpdate.as_view(), name='pedidoweb_edit'),

    url(r'^create/$', views.order_create, name='order_create'),
    # Pedido Tipo: E-Commerce
    # url(r'', views.ProdutoList.as_view(), name='produto_list'),
    url(r'^produto_list/$', views.ProdutoList.as_view(), name='produto_list'),
    url(r'^produto_list/(?P<categoria_slug>[-\w]+)/$', views.ProdutoList.as_view(), name='produto_list_by_category'),
    # url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.produto_detail, name='produto_detail'),
    url(r'^produto_list/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.produto_detail, name='produto_detail'),
    url(r'^produto_detalhe/(?P<pk>[0-9]+)/$', ProdutoDetalhe.as_view(), name="produto_detalhe"),

    # Index
    path('', views.ProdutoList.as_view(), name='home'),

    # Search PedidoWeb
    url(r'^search_pedidoweb/$', views.search_pedidoweb, name='search_pedidoweb'),


]

urlpatterns = format_suffix_patterns(urlpatterns)

