import secrets

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, FormView, ListView, TemplateView

from config.settings import EMAIL_HOST_USER

from .forms import MailUserCreationForm, MailUserChangeForm, UserLoginForm, UserForm, PasswordRecoveryForm
from .models import MailUser
from .services import email_verification, block_user


# Create your views here.
class UserCreateView(CreateView):
    """ Представление для создания нового пользователя"""
    model = MailUser
    form_class = MailUserCreationForm
    success_url = reverse_lazy("users:email_confirmation")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        user.token = token
        user.save()
        send_mail(
            subject="Подтверждение почты",
            message=f'''Для регистрации на сайте почтовых рассылок перейдите, пожалуйста, по ссылке:
            {url} ''',

            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    model = MailUser
    form_class = UserLoginForm


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """ Представление для списка пользователей"""
    model = MailUser
    template_name = "users/user_list.html"

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджеры").exists() or self.request.user.is_superuser


class UserDetailView(LoginRequiredMixin, DetailView):
    """ Представление информации о пользователе"""
    model = MailUser
    form_class = MailUserChangeForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = MailUser
    form_class = MailUserChangeForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:users")
        else:
            return reverse_lazy("sender:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = MailUser

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:users")
        else:
            return reverse_lazy("sender:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class EmailConfirmationView(TemplateView):
    model = MailUser
    template_name = "users/email_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class PasswordRecoveryView(FormView):
    template_name = "users/password_recovery.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = MailUser.objects.get(email=email)
        password = secrets.token_hex(8)
        user.set_password(password)
        user.save()
        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для редактирования профиля пользователя """
    model = MailUser
    form_class = MailUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('sender:home')

    def get_objects(self, queryset=None):
        return self.request.user


# class RegisterView(CreateView):
#     """ Представление для регистрации нового пользователя """
#     template_name = 'users/register.html'
#     form_class = MailUserCreationForm
#     success_url = reverse_lazy('sender:home')
#
#     def form_valid(self, form):
#         user = form.save()
#         user.is_active = False
#         token = secrets.token_hex(16)
#         user.token = token
#         user.save()
#         host = self.request.get_host()
#         url = f'http://{host}/users/email-confirm/{token}/'
#         send_mail(
#             subject='Подтверждение почты',
#             message=f'''Для регистрации на сайте почтовых рассылок перейдите, пожалуйста, по ссылке:
#             {url}''',
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[user.email],
#             fail_silently=False,
#         )
#         return super().form_valid(form)
#
# def email_verification(request, token):
#     user = get_object_or_404(MailUser, token=token)
#     user.is_active = True
#     user.save()
#     return redirect(reverse('users:login'))
#
#
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для редактирования профиля пользователя """
    model = MailUser
    form_class = MailUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('sender:home')

    def get_objects(self, queryset=None):
        return self.request.user
