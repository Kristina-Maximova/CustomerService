import secrets

# from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import MailUserChangeForm, MailUserCreationForm, PasswordRecoveryForm, UserLoginForm
from .models import MailUser


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
        return self.request.user.groups.filter(name="Managers").exists() or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
        return context


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


class BlockUserView(View):
    def post(self, request, pk):
        block_user = MailUser.objects.get(pk=pk)
        if not request.user.has_perm("users.can_block_users"):
            raise PermissionDenied("У вас нет прав блокировать пользователя")

        # Проверка, чтобы пользователь не мог заблокировать сам себя или админа
        if request.user.pk == pk or block_user.is_superuser:
            return HttpResponseRedirect(reverse("users:users"))

        block_user.is_active = not block_user.is_active
        block_user.save()
        return HttpResponseRedirect(reverse("users:users"))
