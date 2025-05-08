from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Addressee, Mailing, Message, SendTry


# Create your views here.
class AddresseeCreateView(CreateView):
    """ Отображение получателя почты"""
    model = Addressee
    fields = ['email', 'full_name', 'comment']
    template_name = 'sender/addressee_form.html'
    success_url = reverse_lazy('sender:home')


class AddresseeUpdateView(UpdateView):
    model = Addressee
    fields = ['email', 'full_name', 'comment']
    template_name = 'sender/addressee_form.html'
    success_url = reverse_lazy('sender:home')


class AddresseeDetailView(DetailView):
    model = Addressee
    template_name = 'sender/addressee_detail.html'
    context_object_name = 'addressee'


class AddresseeDeleteView(DeleteView):
    model = Addressee
    template_name = 'sender/addressee_confirm_delete.html'
    success_url = reverse_lazy('sender:home')


def home_view(request):
    return render(request, 'sender/home.html')
