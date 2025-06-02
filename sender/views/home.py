from django.views.generic import TemplateView

from ..models import Addressee, Mailing


class HomeView(TemplateView):
    """ Представление для главной страницы """
    template_name = 'sender/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = Mailing.objects.count()
        started_mailings = Mailing.objects.filter(status="started").count()
        addressees = Addressee.objects.count()
        context['mailings'] = mailings
        context['started_mailings'] = started_mailings
        context['addressees'] = addressees
        return context
