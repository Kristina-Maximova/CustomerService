from django import forms
from django.forms import BooleanField

from .models import Addressee, Message, Mailing, SendTry


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

    class Meta:
        model = Mailing
        fields = ['message', 'addressees']
        widgets = {
            'addressees': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        # self.fields['start_at'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Время начала'})
        # self.fields['completed_at'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Время завершения'})
        # self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'статус'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'сообщение'})



# class MailingForm(forms.Form):
#     """ Форма для рассылки """
#     start_at = forms.DateTimeField(required=False, label='Время начала: ')
#     completed_at = forms.DateTimeField(required=False, label='Время окончания: ')
#     status = forms.ChoiceField(required=False,  label='Статус' )
#     message = forms.ChoiceField(label='Сообщение')
#     addressees = forms.ChoiceField()


class SendTry(forms.ModelForm):
    """ Форма для попытки рассылки """

    class Meta:
        model = SendTry
        fields = ['mailing']
