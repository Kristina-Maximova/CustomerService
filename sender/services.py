import smtplib

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from config.settings import EMAIL_HOST_USER

from .models import Mailing, SendTry


class MailingService:
    """ Методы обработки отправки почты """

    @staticmethod
    def send_mailing(request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        subject = mailing.message.subject
        message = mailing.message.text
        addressees = [addressee.email for addressee in mailing.addressees.all()]
        user = mailing.owner

        start_at = timezone.now()

        try:
            response = send_mail(
                subject, message, EMAIL_HOST_USER, recipient_list=addressees, fail_silently=False
            )
        except smtplib.SMTPException as e:
            MailingService.try_to_send(
                status="failure", response=e, mailing=mailing
            )
        else:
            completed_at = timezone.now()
            MailingService.try_to_send(
                status="success", response=response, mailing=mailing, user=user
            )
            MailingService.update_status(
                mailing=mailing,
                start_at=start_at,
                completed_at=completed_at,
            )
        finally:
            return redirect(reverse("sender:mailings_list"))

    @staticmethod
    def try_to_send(status, response, mailing, user):
        attempt = SendTry.objects.create(
            try_at=timezone.now(),
            status=status,
            response=response,
            mailing=mailing,
            owner=user
        )
        attempt.save()

    @staticmethod
    def update_status(mailing, start_at, completed_at):
        mailing.start_at = timezone.localtime(start_at)
        mailing.completed_at = timezone.localtime(completed_at)
        mailing.status = "started"
        mailing.save()
