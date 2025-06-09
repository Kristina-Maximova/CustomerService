from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MailUser(AbstractUser):
    """ Модель пользователя почтовой рассылки"""

    username = None
    email = models.EmailField(unique=True, verbose_name='Email',
                              help_text='Введите эл.почту')
    phone = PhoneNumberField(region="RU",
                             blank=True, null=True,
                             verbose_name='Телефон',
                             help_text='Введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/',
                               blank=True, null=True,
                               verbose_name='Аватар',
                               help_text='Загрузите фото, по-желанию')
    country = models.CharField(max_length=25, verbose_name='Страна',
                               help_text='Ваша страна',
                               blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name='Токен',
                             blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_block_users', 'Can block users'),
        ]
