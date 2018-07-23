from django.contrib.auth.models import User
from import_export import resources


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = fields = ('first_name', 'last_name', 'email')

