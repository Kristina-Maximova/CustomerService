from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import MailUserCreationForm, MailUserChangeForm
from .models import MailUser

# Create your views here.
class RegisterView(CreateView):
    """ Представление для регистрации нового пользователя """
    template_name = 'users/register.html'
    form_class = MailUserCreationForm
    success_url = reverse_lazy('sender:home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для редактирования профиля пользователя """
    model = MailUser
    form_class = MailUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('sender:home')

    def get_objects(self, queryset=None):
        return self.request.user

