from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from ..models import Mailing, SendTry


class AttemptsListView(LoginRequiredMixin, ListView):
    model = SendTry
    template_name = 'sender/sendtry/attempts.html'
    context_object_name = 'attempts'

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


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'sender/sendtry/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailings = Mailing.objects.filter(owner=user)
        attempts = SendTry.objects.filter(mailing__in=mailings)

        context['attempts_total'] = attempts.count()
        context['ok'] = attempts.filter(status='success').count()
        context['failure'] = attempts.filter(status='failure').count()
        context['mailings_count'] = mailings.count()

        return context
