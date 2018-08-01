from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # pedidos = serializers.HyperlinkedRelatedField(many=True, view_name='pedidoweb-detail', read_only=True,
    #                                              lookup_field='pedidoweb_id')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'groups', ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
