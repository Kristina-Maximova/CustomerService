from tempfile import template

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


class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'text']
    template_name = 'sender/message/message_form.html'
    success_url = reverse_lazy('sender:messages_list')

class MessageListView(ListView):
    model = Message
    template_name = 'sender/message/messages_list.html'
    context_object_name = 'messages'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'sender/message/message_detail.html'
    context_object_name = 'message'

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'text']
    template_name = 'sender/message/message_form.html'
    success_url = reverse_lazy('sender:messages_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'sender/message/message_confirm_delete.html'
    success_url = reverse_lazy('sender:messages_list')


class MailingCreateView(CreateView):
    model = Mailing
    fields = []


def home_view(request):
    return render(request, 'sender/home.html')
