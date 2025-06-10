import logging

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from ..models import Addressee, Mailing

logger = logging.getLogger('my_logger')


@method_decorator(cache_page(15), name='dispatch')
class HomeView(TemplateView):
    """ Представление для главной страницы """
    template_name = 'sender/home.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Проверяем, авторизован ли пользователь
        if self.request.user.is_authenticated:
            context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
            logger.info('Зашел зарегистрированный пользователь')
            if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser:
                mailings = Mailing.objects.count()
                started_mailings = Mailing.objects.filter(status="started").count()
                addressees = Addressee.objects.count()
                context['mailings'] = mailings
                context['started_mailings'] = started_mailings
                context['addressees'] = addressees
            else:
                mailings = Mailing.objects.filter(owner=self.request.user).count()
                started_mailings = Mailing.objects.filter(Q(status="started") & Q(owner=self.request.user)).count()
                addressees = Addressee.objects.filter(owner=self.request.user).count()
                context['mailings'] = mailings
                context['started_mailings'] = started_mailings
                context['addressees'] = addressees
        logger.info('Зашел незарегистрированный пользователь')
        return context

# c лайва: подумать про UserPassesTestMixin:
# from django.contrib.auth.mixins import UserPassesTestMixin
# from django.views.generic import View
#
#
# class MyView(UserPassesTestMixin, View):
#     # тут надо определить test_func с проверкой (проверка может быть любая)
#     def test_func(self):
#         return self.request.user.email.endswith('@.example.com')
