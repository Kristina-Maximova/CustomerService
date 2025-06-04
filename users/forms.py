from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from django.urls import reverse_lazy

from sender.forms import StyleFormMixin
from .models import MailUser


class MailUserCreationForm(StyleFormMixin, UserCreationForm):
    """ Форма для регистрации нового пользователя"""

    class Meta(UserCreationForm.Meta):
        model = MailUser
        fields = ('email', 'password1', 'password2',)


class MailUserChangeForm(StyleFormMixin, forms.ModelForm):
    """ Форма для редактирования профиля пользователя"""

    class Meta(UserCreationForm.Meta):
        model = MailUser
        fields = ('email', 'password', 'phone', 'avatar', 'country')
        success_url = reverse_lazy("users:users")


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = MailUser
        fields = ('email', 'phone', 'avatar', 'country',)


class PasswordRecoveryForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label="Укажите Email")


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    model = MailUser
