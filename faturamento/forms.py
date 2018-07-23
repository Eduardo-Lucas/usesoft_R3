from django.forms import forms

from faturamento.models import Participante


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['cnpj_cpf', 'fisica_juridica', 'cep', 'razao_social', 'nome_fantasia', 'telefone', 'telefone2',
                  'celular', 'email', 'endereco', 'complemento', 'numero', 'bairro', 'cidade', 'estado',
                  'inscricao_estadual', 'inscricao_municipal']

