from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import MailingForm
from ..models import Mailing
from ..services import MailingService


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

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


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'sender/mailing/mailings_list.html'
    context_object_name = 'mailings'

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


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'sender/mailing/mailing_form.html'
    success_url = reverse_lazy('sender:mailings_list')

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MailingForm
        raise PermissionDenied

    # @staticmethod
    # def stop_mailshot(request, pk):
    #     stopped_mailshot = Mailing.objects.get(pk=pk)
    #
    #     stopped_mailshot.status = "completed"
    #     stopped_mailshot.save()
    #     return redirect(reverse("sender:mailing_list"))


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'sender/mailing/mailing_detail.html'
    context_object_name = 'mailing'


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'sender/mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('sender:mailings_list')


class SendMailing(View):
    """ Отправка почтовых сообщений """
    model = Mailing
    template_name = 'sender/mailing/mailing_list.html'
    context_object_name = 'mailing'

    # print("Вызов метода SendMailing произошел")

    def post(self, request, pk):
        # print(f"POST method called with pk: {pk}")
        MailingService.send_mailing(request, pk)
        return redirect(reverse("sender:mailings_list"))


class StopMailingView(View):
    """ Переводит рассылку в статус (завершена) """

    def post(self, request, pk):
        stoped_mailing = Mailing.objects.get(pk=pk)
        if not request.user.has_perm("sender.can_stop_mailing"):
            raise PermissionDenied("У вас нет прав останавливать рассылки")

        stoped_mailing.status = 'completed'

        stoped_mailing.save()
        return HttpResponseRedirect(reverse("sender:mailings_list"))
