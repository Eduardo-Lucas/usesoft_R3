from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from accounts.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Usuários, ou cria um novo Usuário.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    Lista todos os Grupos, ou cria um novo Grupo.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

