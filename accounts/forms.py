from django import forms

from django.http import request
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha  ', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("O usuário e/ou senha estão incorretos!")
        return super(UserLoginForm, self).clean(*args, **kwargs)
