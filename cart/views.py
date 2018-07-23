from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from materiais.models import Produto
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, produto_id):
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        if cd['update'] is False:
            if cd['desconto'] > 0:
                desconto = cd['desconto']
            else:
                # =100-((PREÇO_SUGERIDO*100)/PREÇO_VENDA)
                desconto = 100 - ((cd['preco_negociado']*100) / produto.preco_venda)

            if desconto <= 30:
                cart.add(produto=produto,
                         quantity=cd['quantity'],
                         preco_negociado=cd['preco_negociado'],
                         update_quantity=cd['update'],
                         desconto=desconto)
                messages.success(request, 'Produto ' + produto.produto + produto.descricao + ' colocado no carrinho.')
            else:
                messages.error(request, 'O produto '+str(produto.produto)+' com preço de venda R$ ' +
                               str(produto.preco_venda)+' e preço negociado a R$' +
                               str(cd['preco_negociado']))
                messages.error(request, 'Gerou um percentual de desconto de '+str(desconto) +
                               '% que está acima do limite máximo permitido ')
                messages.error(request, 'Por esse motivo, o produto não foi colocado no carrinho.')
        else:
            cart.add(produto=produto,
                     quantity=cd['quantity'],
                     preco_negociado=cd['preco_negociado'],
                     update_quantity=cd['update'],
                     desconto=cd['desconto'])

    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, produto_id):
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    cart.remove(produto)
    messages.success(request, 'Produto ' + produto.produto + produto.descricao + ' removido do carrinho.')

    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'preco_negociado': item['preco_unitario'],
                     'update': True,
                     'perc_desc':
                         100.00 - ((float(item['preco_unitario'])*100)/float(item['price'])),
                     # 'perc_desc': item['perc_desc'],
                     'valor_desconto':
                     (item['price'] * (item['perc_desc']/100)) *
                     item['quantity']
                     })
    return render(request, 'cart/detail.html', {'cart': cart})
