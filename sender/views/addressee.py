from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from ..models import Addressee
from ..forms import AddresseeForm


class AddresseeCreateView(LoginRequiredMixin, CreateView):
    """ Отображение получателя почты"""
    model = Addressee
    form_class = AddresseeForm
    template_name = 'sender/addressee/addressee_form.html'
    success_url = reverse_lazy('sender:addressees_list')

    def form_valid(self, form):
        addressee = form.save()
        user = self.request.user
        addressee.owner = user
        addressee.save()

        return super().form_valid(form)


class AddresseeUpdateView(LoginRequiredMixin, UpdateView):
    model = Addressee
    form_class = AddresseeForm
    template_name = 'sender/addressee/addressee_form.html'
    success_url = reverse_lazy('sender:addressees_list')


class AddresseeDetailView(DetailView):
    model = Addressee
    template_name = 'sender/addressee/addressee_detail.html'
    context_object_name = 'addressee'


class AddresseeDeleteView(LoginRequiredMixin, DeleteView):
    model = Addressee
    template_name = 'sender/addressee/addressee_confirm_delete.html'
    success_url = reverse_lazy('sender:addressees_list')


class AddresseeListView(ListView):
    model = Addressee
    template_name = 'sender/addressee/addressees_list.html'
    context_object_name = 'addressees'
