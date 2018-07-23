"""
    Participante - GENERIC VIEWS
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from faturamento.models import Participante


class ParticipanteList(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Participante
    template_name = 'faturamento/participante/participante_list.html'

    def get_queryset(self):
        valor = self.request.GET.get('q')
        if valor:
            object_list = self.model.objects.filter(
                Q(razao_social__icontains=valor) |
                Q(nome_fantasia__icontains=valor) |
                Q(codigo__contains=valor) |
                Q(cnpj_cpf__contains=valor)
            )
        else:
            object_list = self.model.objects.all()

        paginator = Paginator(object_list, 7)  # Show 7 produtos per page

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


class ParticipanteDetalhe(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Participante
    template_name = 'faturamento/participante/participante_detail.html'


class ParticipanteCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Participante
    fields = '__all__'
    success_message = 'Registro criado com sucesso!'
    template_name = "faturamento/participante/participante_form.html"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.id
        )


class ParticipanteUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Participante
    fields = '__all__'
    success_message = 'Registro alterado com sucesso!'
    template_name = 'faturamento/participante/participante_form.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.id
        )


def participante_delete(request, id=None):
    obj = get_object_or_404(Participante, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Registro apagado com sucesso!')
        return redirect('faturamento:participante_list')

    context = {
        'object': obj
    }

    return render(request, 'faturamento/confirm_delete.html', context)
