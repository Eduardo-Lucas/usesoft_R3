"""usesoft_R3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from django.urls import path, include
from rest_framework import routers

from accounts.views import login_view, logout_view
from django.conf.urls.static import static
from usesoft_R3 import settings

from materiais import api_views as materiais_api
from globais import api_views as globais_api
from financeiro import api_views as financeiro_api
from faturamento import api_views as faturamento_api
from accounts import api_views as accounts_api

router = routers.DefaultRouter()
router.register(r'pedidosweb', materiais_api.PedidoWebViewSet)
router.register(r'pedidowebitens', materiais_api.PedidoWebItemViewSet)
router.register(r'cfops', globais_api.CfopViewSet)
router.register(r'municipios', globais_api.MunicipioViewSet)
router.register(r'estados', globais_api.UfViewSet)
router.register(r'paises', globais_api.PaisIbgeViewSet)
router.register(r'tiposoperacoesfiscais', globais_api.TipoOperacaoFiscalViewSet)
router.register(r'tipospagamento', financeiro_api.TipoPagamentoViewSet)
router.register(r'prazospagamento', financeiro_api.PrazoPagamentoViewSet)
router.register(r'tiposdocumentos', financeiro_api.TipoDocumentoViewSet)
router.register(r'participantes', faturamento_api.ParticipanteViewSet)
router.register(r'gruposparticipantes', faturamento_api.GrupoParticipanteViewSet)
router.register(r'regioesdevenda', faturamento_api.RegiaoDeVendaViewSet)
router.register(r'usuarios', accounts_api.UserViewSet)
router.register(r'grupos', accounts_api.GroupViewSet)
router.register(r'mensagenspadrao', globais_api.MensagemPadraoViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'),),
    path('admin/', admin.site.urls),
    url(r'^cart/', include('cart.urls')),
    url(r'^faturamento/', include('faturamento.urls')),
    url(r'^financeiro/', include('financeiro.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^', include('materiais.urls')),
    url(r'^login', login_view, name='login'),
    url(r'^logout', logout_view, name='logout'),
    # url(r'^change-password', change_password, name='change_password'),
    url(r'^reset-password/$', password_reset, name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete, name='password_reset_complete'),



    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

