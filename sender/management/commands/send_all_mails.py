from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from config.settings import EMAIL_HOST_USER

from ...models import Mailing, SendTry


class Command(BaseCommand):
    help = "Отправка всех рассылок"

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status__in=[Mailing.CREATED, Mailing.STARTED])
        for mailing in mailings:
            for addressee in mailing.addressees.all():
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.text,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[addressee.email],
                        fail_silently=False,
                    )
                    SendTry.objects.create(
                        try_at=timezone.now(),
                        status='success',
                        response="Email отправлен",
                        mailing=mailing,
                    )
                    print(f"Сообщение {mailing.message.subject} успешно отправлено на  {addressee.email}")
                except Exception as e:
                    SendTry.objects.create(
                        try_at=timezone.now(),
                        status='failure',
                        response=str(e),
                        mailing=mailing,
                    )
                    print(str(e))
                mailing.save()
