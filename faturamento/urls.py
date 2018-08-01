from django.conf.urls import url

from faturamento import api_views
from faturamento.views import ParticipanteList, ParticipanteDetalhe, ParticipanteCreate, ParticipanteUpdate, \
    participante_delete

app_name = 'faturamento'

urlpatterns = [

    # Participante
    url(r'^participante_list/$', ParticipanteList.as_view(), name='participante_list'),
    url(r'^participante_list/(?P<pk>[0-9]+)/$', ParticipanteDetalhe.as_view(), name='participante_detail'),
    url(r'^participante_add/$', ParticipanteCreate.as_view(), name='participante_add'),
    url(r'^participante/(?P<pk>[0-9]+)/edit/$', ParticipanteUpdate.as_view(), name='participante_edit'),
    url(r'^participante/(?P<id>[0-9]+)/delete/$', participante_delete, name='participante_delete'),


]
