from decimal import Decimal
from unicodedata import decimal

from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from requests import request

from materiais.models import Produto, ProdutoTributacao


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Produto.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['perc_desc'] = Decimal(item['perc_desc'])
            item['valor_desconto'] = Decimal(item['price'] * (Decimal(item['perc_desc'])/Decimal(100))) * item['quantity']
            item['total_price'] = Decimal((item['price'] - (item['price'] * (Decimal(item['perc_desc'])/Decimal(100)))) * item['quantity'])
            yield item

    def add(self, produto, quantity=1, preco_negociado=0, update_quantity=False, desconto=0):
        """
        Add a product to the cart or update its quantity.
        """

        produto_id = str(produto.id)

        produto_tributacao = ProdutoTributacao.objects.get(produto=produto_id)

        if produto_id not in self.cart:

            if desconto >= 0:
                desconto = desconto
            else:
                desconto = 100 - ((preco_negociado * 100) / produto.preco_venda)

            # Boolean invertido   False=True  e  True=False
            if desconto <= 0:
                desconto_negativo = False
            else:
                desconto_negativo = True
            print('Desconto negativo ==> '+str(desconto_negativo))

            if desconto > 30:
                excedeu_limite_maximo = True
            else:
                excedeu_limite_maximo = False

            total_produto = (float(produto.preco_venda) - (float(produto.preco_venda) * (int(desconto) / 100))) * int(
                quantity)

            self.cart[produto_id] = {'sequencia': 0,
                                     'codigo': str(produto.produto),
                                     'unidade': str(produto.unidade),
                                     'descricao': str(produto.descricao),
                                     'observacoes': ' ',
                                     # corresponde ao CFOP 5102 => id=2046
                                     'cfop': 5102,
                                     'codigo_ncm': str(produto.codigo_ncm),
                                     'codigo_cest': str(produto.codigo_cest),
                                     'status_pedido_item': 'W',
                                     'autorizacao_faturamento': ' ',
                                     'autorizacao_numitem': 0,
                                     'quantity': 0,
                                     'peso_liquido': str(produto.peso_liquido),
                                     'peso_bruto': str(produto.peso_bruto),
                                     'metro_cubico': str(produto.altura * produto.largura * produto.comprimento),
                                     'movimenta_estoques': 'N',
                                     'saldo_fisico': 0,
                                     'saldo_fiscal': 0,
                                     'preco_custo': 0,
                                     'preco_medio': 0,
                                     'preco_custo_nfe': 0,
                                     'preco_medio_nfe': 0,
                                     'preco_unitario': str(produto.preco_venda),
                                     # desconto
                                     'perc_desc': str(desconto),
                                     'custo_informado': 0,
                                     'data_movimento': str(timezone.now()),
                                     'participante': str(produto.fabricante),
                                     'total_produto': str(total_produto),
                                     'modalidade_ipi': 0,
                                     'situacao_tributaria_ipi': str(produto_tributacao.situacao_tributaria_ipi),
                                     'base_calc_ipi': 0,
                                     'perc_ipi': 0,
                                     'perc_red_ipi': 0,
                                     'modalidade_calculo': 0,
                                     'modalidade_icms': 0,
                                     'situacao_tributaria_icms': str(produto_tributacao.situacao_tributaria_icms),
                                     'base_calc_icms': 0,
                                     'perc_icms': 0,
                                     'perc_antec_tributaria': 0,
                                     'perc_red_icms': 0,
                                     'modalidade_calculo_subst': 0,
                                     'base_calc_icms_sub': 0,
                                     'perc_mva_sub': 0,
                                     'perc_icms_sub': 0,
                                     'base_calc_antecipacao_trib': 0,
                                     'perc_antecipacao_trib': 0,
                                     'situacao_tributaria_pis': str(produto_tributacao.situacao_tributaria_pis),
                                     'base_calc_pis': 0,
                                     'perc_pis': 0,
                                     'situacao_tributaria_cofins': str(produto_tributacao.situacao_tributaria_cofins),
                                     'base_calc_cofins': 0,
                                     'perc_fundo_pobreza': 0,
                                     'perc_trib_aproximado': 0,
                                     'base_calc_import': 0,
                                     'perc_import': 0,
                                     'base_calc_issqn': 0,
                                     'perc_issqn': 0,
                                     'perc_desp_acessorias': 0,
                                     'perc_seguro': 0,
                                     'perc_frete': 0,
                                     'natureza_custos': 1,
                                     'centro_custo': 1,
                                     'codigo_promocao': 0,
                                     'excedeu_limite_maximo': excedeu_limite_maximo,
                                     'desconto_negativo': desconto_negativo,
                                     'price': str(produto.preco_venda)}

        if update_quantity:
            self.cart[produto_id]['quantity'] = quantity
        else:
            self.cart[produto_id]['quantity'] += quantity
        self.save()

    def remove(self, produto):
        """
        Remove a product from the cart.
        """
        produto_id = str(produto.id)
        if produto_id in self.cart:
            del self.cart[produto_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        # return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

        return sum(
            (Decimal(item['price']) - (Decimal(item['price']) * (Decimal(item['perc_desc'])/Decimal(100.00)
                                                                 )
                                       )
             ) * item['quantity'] for item in self.cart.values()
        )

