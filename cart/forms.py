from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]
DESCONTO_CHOICES = [(i, str(i)) for i in range(0, 31)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Quantidade', choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    desconto = forms.TypedChoiceField(choices=DESCONTO_CHOICES, coerce=int, required=False)
    preco_negociado = forms.DecimalField(label='Preço Líquido', decimal_places=2, required=False, initial=True)
