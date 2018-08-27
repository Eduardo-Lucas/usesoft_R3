from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db import transaction
from django.db.models import Q

from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from cart.cart import Cart
from cart.forms import CartAddProductForm
from faturamento.models import Participante

from materiais.filters import PedidoWebFilter
from materiais.forms import OrderCreateForm, PedidoWebFormSet
from materiais.models import Produto, PedidoWebItem, PedidoWeb


@login_required
def home(request):
    return render(request, 'materiais/produto/list.html')


"""
  TELA DE EMISSÃO DE PEDIDO TIPO E-COMMERCE
"""


class ProdutoCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Produto
    fields = '__all__'
    template_name = 'materiais/produto/produto_form.html'


class ProdutoList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Produto
    context_object_name = 'produtos'
    template_name = 'materiais/produto/list.html'

    def get_queryset(self):
        valor = self.request.GET.get('q')
        if valor:
            object_list = self.model.objects.filter(
                Q(produto__icontains=valor) |
                Q(descricao__icontains=valor) |
                Q(preco_venda__icontains=valor) |
                Q(categoria__nome__icontains=valor)
            )
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 2)  # Show 2 produtos per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


# @login_required
# def produto_list(request, categoria_slug=None):
#     categoria = None
#     categorias = Categoria.objects.all()
#     produtos = Produto.objects.filter(disponivel='S')
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(produtos, 10)
#     try:
#         produtos = paginator.page(page)
#     except PageNotAnInteger:
#         produtos = paginator.page(1)
#     except EmptyPage:
#         produtos = paginator.page(paginator.num_pages)
#
#     if categoria_slug:
#         categoria = get_object_or_404(Categoria, slug=categoria_slug)
#         produtos = produtos.filter(categoria=categoria)
#
#     return render(request, 'materiais/produto/list.html', {'categoria': categoria,
#                                                            'categorias': categorias,
#                                                            'produtos': produtos})


@login_required()
def produto_detail(request, id=None, slug=None):
    produto = get_object_or_404(Produto, id=id, slug=slug, disponivel='S')
    cart_produto_form = CartAddProductForm(initial={'preco_negociado': produto.preco_venda})
    return render(request, 'materiais/produto/detail.html', {'produto': produto,
                                                             'cart_produto_form': cart_produto_form})


class ProdutoDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Produto
    context_object_name = 'produto'
    template_name = 'materiais/produto/produto_detail.html'


@login_required()
def novo_pedido(request):
    return render(request, 'materiais/pedido/novopedido.html')


@login_required()
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            pedidoweb = form.save(commit=False)

            # TODO Se o usuario for do Grupo Vendedor, já preenche o campo vendedor
            # TODO Caso contrário, Usuário precisa escolher o vendedor da lista

            if request.user.groups == "Clientes":
                pedidoweb.vendedor = request.user
                pedidoweb.participante = Participante.objects.get(vendedor=request.user)

            pedidoweb.total_produtos = cart.get_total_price()
            pedidoweb.save()

            seq = 0
            for item in cart:

                seq += 1
                PedidoWebItem.objects.create(pedidoweb=pedidoweb,
                                             sequencia=seq,
                                             produto=item['product'],
                                             unidade=item['unidade'],
                                             descricao=item['descricao'],
                                             observacoes=item['observacoes'],
                                             cfop=item['cfop'],
                                             codigo_ncm=item['codigo_ncm'],
                                             codigo_cest=item['codigo_cest'],
                                             status_pedido_item=item['status_pedido_item'],
                                             autorizacao_faturamento=item['autorizacao_faturamento'],
                                             autorizacao_numitem=item['autorizacao_numitem'],
                                             quantidade=item['quantity'],
                                             peso_liquido=item['peso_liquido'],
                                             peso_bruto=item['peso_bruto'],
                                             metro_cubico=item['metro_cubico'],
                                             movimenta_estoques=item['movimenta_estoques'],
                                             saldo_fisico=item['saldo_fisico'],
                                             saldo_fiscal=item['saldo_fiscal'],
                                             preco_custo=item['preco_custo'],
                                             preco_medio=item['preco_medio'],
                                             preco_custo_nfe=item['preco_custo_nfe'],
                                             preco_medio_nfe=item['preco_medio_nfe'],
                                             preco_unitario=item['price'],
                                             perc_desc=item['perc_desc'],
                                             custo_informado=item['custo_informado'],
                                             data_movimento=item['data_movimento'],
                                             participante=pedidoweb.participante,
                                             total_produto=item['total_produto'],
                                             modalidade_ipi=item['modalidade_ipi'],
                                             situacao_tributaria_ipi=item['situacao_tributaria_ipi'],
                                             base_calc_ipi=item['base_calc_ipi'],
                                             perc_ipi=item['perc_ipi'],
                                             perc_red_ipi=item['perc_red_ipi'],
                                             modalidade_calculo=item['modalidade_calculo'],
                                             modalidade_icms=item['modalidade_icms'],
                                             situacao_tributaria_icms=item['situacao_tributaria_icms'],
                                             base_calc_icms=item['base_calc_icms'],
                                             perc_icms=item['perc_icms'],
                                             perc_antec_tributaria=item['perc_antec_tributaria'],
                                             perc_red_icms=item['perc_red_icms'],
                                             modalidade_calculo_subst=item['modalidade_calculo_subst'],
                                             base_calc_icms_sub=item['base_calc_icms_sub'],
                                             perc_mva_sub=item['perc_mva_sub'],
                                             perc_icms_sub=item['perc_icms_sub'],
                                             base_calc_antecipacao_trib=item['base_calc_antecipacao_trib'],
                                             perc_antecipacao_trib=item['perc_antecipacao_trib'],
                                             situacao_tributaria_pis=item['situacao_tributaria_pis'],
                                             base_calc_pis=item['base_calc_pis'],
                                             perc_pis=item['perc_pis'],
                                             situacao_tributaria_cofins=item['situacao_tributaria_cofins'],
                                             base_calc_cofins=item['base_calc_cofins'],
                                             perc_fundo_pobreza=item['perc_fundo_pobreza'],
                                             perc_trib_aproximado=item['perc_trib_aproximado'],
                                             base_calc_import=item['base_calc_import'],
                                             perc_import=item['perc_import'],
                                             base_calc_issqn=item['base_calc_issqn'],
                                             perc_issqn=item['perc_issqn'],
                                             perc_desp_acessorias=item['perc_desp_acessorias'],
                                             perc_seguro=item['perc_seguro'],
                                             perc_frete=item['perc_frete'],
                                             natureza_custos=item['natureza_custos'],
                                             centro_custo=item['centro_custo'],
                                             codigo_promocao=item['codigo_promocao']
                                             )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            return render(request, 'materiais/pedido/created.html', {'pedidoweb': pedidoweb})
    else:
        form = OrderCreateForm()
    return render(request, 'materiais/pedido/create.html', {'cart': cart,
                                                            'form': form})


"""
  TELA DE EMISSÃO DE PEDIDO TIPO TRADICIONAL
"""


class PedidoWebTradicionalList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = PedidoWeb
    template_name = 'materiais/pedido/pedidoweb_list.html'

    def get_queryset(self):
        valor = self.request.GET.get('q')
        if valor:
            object_list = self.model.objects.filter(
                Q(participante__razao_social__icontains=valor) |
                Q(prazo_de_pagamento__descricao__icontains=valor) |
                Q(id__icontains=valor) |
                Q(tipo_de_pagamento__descricao__icontains=valor) |
                Q(pedidowebitem__preco_unitario__icontains=valor) |
                Q(observacoes__icontains=valor)
            )
        else:
            # this returns the first 100 objects (LIMIT 100):
            if self.request.user.is_superuser:
                object_list = self.model.objects.all()[:100]
            else:
                object_list = self.model.objects.filter(vendedor=self.request.user)[:100]

        paginator = Paginator(object_list, 6)  # Show 6 pedidos per page

        page = self.request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        # return object_list
        return queryset


class PedidoWebTradicionalCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PedidoWeb
    context_object_name = 'pedidoweb'
    fields = ['participante', 'vendedor', 'tipo_de_pagamento', 'prazo_de_pagamento']
    success_url = reverse_lazy('materiais:pedidoweb_list')
    template_name = 'materiais/pedido/pedidoweb_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.id,
        )

    def get_context_data(self, **kwargs):
        data = super(PedidoWebTradicionalCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['pedidoweb_item'] = PedidoWebFormSet(self.request.POST)
        else:
            data['pedidoweb_item'] = PedidoWebFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        pedidoweb_item = context['pedidoweb_item']

        with transaction.atomic():
            if pedidoweb_item.is_valid():
                self.object = form.save()
                pedidoweb_item.instance = self.object
                pedidoweb_item.save()
                messages.success(self.request, 'Pedido criado com sucesso!')

        return super(PedidoWebTradicionalCreate, self).form_valid(form)


class PedidoWebTradicionalDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = PedidoWeb
    context_object_name = 'pedidoweb'
    template_name = 'materiais/pedido/pedidoweb_detail.html'


class PedidoWebTradicionalUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PedidoWeb
    fields = ['participante', 'tipo_de_pagamento', 'prazo_de_pagamento', ]
    template_name = 'materiais/pedido/pedidoweb_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.id,
        )


def search_pedidoweb(request):
    if request.user.is_superuser:
        pedidoweb_list = PedidoWeb.objects.all()
    else:
        pedidoweb_list = PedidoWeb.objects.filter(vendedor=request.user)

    pedidoweb_filter = PedidoWebFilter(request.GET, queryset=pedidoweb_list)
    return render(request, 'materiais/search_pedidoweb/pedidoweb_filter_list.html', {'filter': pedidoweb_filter})
