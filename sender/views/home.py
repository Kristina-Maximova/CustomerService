from django.views.generic import TemplateView
from django.db.models import Q

from ..models import Addressee, Mailing


class HomeView(TemplateView):
    """ Представление для главной страницы """
    template_name = 'sender/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = Mailing.objects.filter(owner=self.request.user).count()
        started_mailings = Mailing.objects.filter(Q(status="started") & Q(owner=self.request.user)).count()
        addressees = Addressee.objects.filter(owner=self.request.user).count()
        context['mailings'] = mailings
        context['started_mailings'] = started_mailings
        context['addressees'] = addressees
        return context
