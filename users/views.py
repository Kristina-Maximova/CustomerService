import secrets
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
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

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'''Для регистрации на сайте почтовых рассылок перейдите, пожалуйста, по ссылке: 
{url}''',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(MailUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
        """ Представление для редактирования профиля пользователя """
        model = MailUser
        form_class = MailUserChangeForm
        template_name = 'users/profile_update.html'
        success_url = reverse_lazy('sender:home')

        def get_objects(self, queryset=None):
            return self.request.user
