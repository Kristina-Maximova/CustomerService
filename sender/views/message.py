from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import MessageForm
from ..models import Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'sender/message/message_form.html'
    success_url = reverse_lazy('sender:messages_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()

        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'sender/message/messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'sender/message/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    # fields = ['subject', 'text']
    template_name = 'sender/message/message_form.html'
    success_url = reverse_lazy('sender:messages_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'sender/message/message_confirm_delete.html'
    success_url = reverse_lazy('sender:messages_list')
