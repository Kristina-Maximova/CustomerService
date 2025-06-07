from django.core.exceptions import PermissionDenied
from django.http import request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Mailing
from ..forms import MailingForm
from ..services import MailingService


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm

    # fields = ['start_at', 'completed_at', 'status', 'message', 'addressees']
    template_name = 'sender/mailing/mailing_form.html'
    success_url = reverse_lazy('sender:mailings_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()

        return super().form_valid(form)

    # def form_valid(self, form):
    #     mailing = form.save(commit=False)  # Сохраняем форму без сохранения в БД
    #     mailing.owner = self.request.user
    #     mailing.save()  # Теперь сохраняем в БД
    #
    #     return super().form_valid(form)

class MailingListView(ListView):
    model = Mailing
    template_name = 'sender/mailing/mailings_list.html'
    context_object_name = 'mailings'


    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(owner=self.request.user)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    # fields = ['start_at', 'completed_at', 'status', 'message', 'addressees']
    template_name = 'sender/mailing/mailing_form.html'
    success_url = reverse_lazy('sender:mailings_list')

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MailingForm
        raise PermissionDenied

    @staticmethod
    def stop_mailshot(request, pk):
        stopped_mailshot = Mailing.objects.get(pk=pk)

        stopped_mailshot.status = "completed"
        stopped_mailshot.save()
        return redirect(reverse("sender:mailing_list"))


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'sender/mailing/mailing_detail.html'
    context_object_name = 'mailing'


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'sender/mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('sender:mailings_list')


class SendMailing(View):
    model = Mailing
    template_name = 'sender/mailing/mailing_list.html'
    context_object_name = 'mailing'
    print("Вызов метода SendMailing произошел")


    def post(self, request, pk):
        print(f"POST method called with pk: {pk}")
        MailingService.send_mailing(request, pk)
        return redirect(reverse("sender:mailings_list"))

