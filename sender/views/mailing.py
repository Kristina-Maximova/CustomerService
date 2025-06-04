from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Mailing
from ..forms import MailingForm


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    # fields = ['start_at', 'completed_at', 'status', 'message', 'addressees']
    template_name = 'sender/mailing/mailing_form.html'
    success_url = reverse_lazy('sender:mailings_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'sender/mailing/mailings_list.html'
    context_object_name = 'mailings'


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    # fields = ['start_at', 'completed_at', 'status', 'message', 'addressees']
    template_name = 'sender/mailing/mailing_form.html'
    success_url = reverse_lazy('sender:mailings_list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'sender/mailing/mailing_detail.html'
    context_object_name = 'mailing'


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'sender/mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('sender:mailings_list')



