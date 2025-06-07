
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Message
from ..forms import MessageForm


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    # fields = ['subject', 'text']
    template_name = 'sender/message/message_form.html'
    success_url = reverse_lazy('sender:messages_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()

        return super().form_valid(form)



class MessageListView(ListView):
    model = Message
    template_name = 'sender/message/messages_list.html'
    context_object_name = 'messages'


    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    template_name = 'sender/message/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    # fields = ['subject', 'text']
    template_name = 'sender/message/message_form.html'
    success_url = reverse_lazy('sender:messages_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'sender/message/message_confirm_delete.html'
    success_url = reverse_lazy('sender:messages_list')
