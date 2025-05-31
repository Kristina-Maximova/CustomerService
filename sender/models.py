from random import choices

from django.db import models


class Addressee(models.Model):
    """ Класс для представления получателя почты """
    email = models.CharField(max_length=150, unique=True, verbose_name='email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    comment = models.TextField(null=True, blank=True, verbose_name='комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'адресат: {self.full_name}'

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['full_name']


class Message(models.Model):
    """ Класс для представления сообщения"""

    subject = models.CharField(max_length=250, verbose_name='тема сообщения', null=True, blank=True)
    text = models.TextField(verbose_name='текст сообщения')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'сообщение {self.pk}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    """ Класс для модели рассылки сообщений """


    number_of_mailing = 0  # переменная-счетчик на уровне класса

    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (CREATED, 'создана'),
        (STARTED, 'запущена'),
        (COMPLETED, 'завершена')
    ]
    start_at = models.DateTimeField(null=True, blank=True,
                                    verbose_name='время запуска')
    completed_at = models.DateTimeField(null=True, blank=True,
                                        verbose_name='время завершения')
    status = models.CharField(max_length=18,
                              choices=STATUS_CHOICES,
                              verbose_name='статус')
    message = models.ForeignKey(Message, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                verbose_name='сообщение')
    addressees = models.ManyToManyField(Addressee, null=True, blank=True,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'рассылка {self.pk}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

class SendTry(models.Model):
    """ Класс для попытки рассылки сообщений"""
    SUCCESS = 'success'
    FAILURE = 'failure'
    STATUS_CHOICES=[
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Не успешно')
    ]

    try_at = models.DateTimeField(null=True, blank=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              verbose_name='статус попытки',
                              null=True, blank=True)
    response = models.TextField(null=True, blank=True, verbose_name='ответ сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                verbose_name='рассылка',
                                null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"попытка рассылки {self.pk}"

    class Meta:
        verbose_name='попытка отправки'
        verbose_name_plural='попытки отправки'

