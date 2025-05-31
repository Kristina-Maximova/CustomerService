from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from ..models import Message

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
