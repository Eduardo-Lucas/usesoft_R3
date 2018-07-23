from collections import UserList

from django.conf.urls import url

from accounts.views import UserprofileList, UserprofileDetalhe, UserprofileUpdate, userprofile_delete

app_name = 'accounts'

urlpatterns = [

    url(r'^userprofile-list/$', UserprofileList.as_view(), name='userprofile-list'),
    url(r'^userprofile-list/(?P<pk>[0-9]+)/$', UserprofileDetalhe.as_view(), name='userprofile-detail'),
    url(r'^userprofile/(?P<pk>[0-9]+)/edit/$', UserprofileUpdate.as_view(), name='userprofile-edit'),
    url(r'^userprofile/(?P<id>[0-9]+)/delete/$', userprofile_delete, name='userprofile-delete'),

]
