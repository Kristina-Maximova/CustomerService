from django import forms
from django.forms import BooleanField

from .models import Addressee, Mailing, Message, SendTry


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # в self.fields() получим словарь: {название поля:значение}
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-label"
            else:
                field.widget.attrs['class'] = "form-control"


class AddresseeForm(StyleFormMixin, forms.ModelForm):
    """ Форма для получателя рассылки """

    class Meta:
        model = Addressee
        fields = ['email', 'full_name', 'comment']


class MessageForm(StyleFormMixin, forms.ModelForm):
    """ Форма для сообщения """

    class Meta:
        model = Message
        fields = ['subject', 'text']


class MailingForm(forms.ModelForm):
    """ Форма для рассылки """

    # c лайва по курсовой:
    # def __init__(self,*args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     user = self.request.user
    #     super().__init__(*args, **kwargs)
    #     self.fields['addressees'].queryset = Addressee.objects.filter(owner=user)
    #     self.fields['message'].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Mailing
        fields = ['message', 'addressees']
        widgets = {
            'addressees': forms.CheckboxSelectMultiple(),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError('Сообщение не должно быть пустым.')
        return message

    def clean_addressees(self):
        addressees = self.cleaned_data.get('addressees')
        if not addressees.exists():  # Для ManyToManyField нужно проверять через exists()
            raise forms.ValidationError('Адресаты не должны быть пустыми.')
        return addressees

    # def __init__(self, *args, **kwargs):
    #     super(MailingForm, self).__init__(*args, **kwargs)
    #     self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'сообщение'})

    def __init__(self, *args, **kwargs):
        # Извлекаем текущего пользователя из kwargs
        self.user = kwargs.pop('user')
        super(MailingForm, self).__init__(*args, **kwargs)
        # Фильтруем сообщения по текущему пользователю
        self.fields['message'].queryset = Message.objects.filter(owner=self.user)
        # Фильтруем адресатов по текущему пользователю
        self.fields['addressees'].queryset = Addressee.objects.filter(owner=self.user)
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'сообщение'})


class SendTryForm(forms.ModelForm):
    """ Форма для попытки рассылки """

    class Meta:
        model = SendTry
        fields = ['mailing']
