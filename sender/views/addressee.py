from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from ..models import Addressee


class AddresseeCreateView(CreateView):
    """ Отображение получателя почты"""
    model = Addressee
    fields = ['email', 'full_name', 'comment']
    template_name = 'sender/addressee/addressee_form.html'
    success_url = reverse_lazy('sender:addressees_list')


class AddresseeUpdateView(UpdateView):
    model = Addressee
    fields = ['email', 'full_name', 'comment']
    template_name = 'sender/addressee/addressee_form.html'
    success_url = reverse_lazy('sender:addressees_list')


class AddresseeDetailView(DetailView):
    model = Addressee
    template_name = 'sender/addressee/addressee_detail.html'
    context_object_name = 'addressee'


class AddresseeDeleteView(DeleteView):
    model = Addressee
    template_name = 'sender/addressee/addressee_confirm_delete.html'
    success_url = reverse_lazy('sender:addressees_list')


class AddresseeListView(ListView):
    model = Addressee
    template_name = 'sender/addressee/addressees_list.html'
    context_object_name = 'addressees'
