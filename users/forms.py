from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField

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
        fields = ('email', 'phone', 'avatar', 'country',)

