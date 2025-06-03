from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import smtplib

from config.settings import  EMAIL_HOST_USER, CACHE_ENABLED
from .models import Mailing, SendTry

class MailingService:
    """ Методы обработки отправки почты """

    @staticmethod
    def send_mailing(request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        subject = mailing.message.subject
        message = mailing.message.text
        addressees = [addressee.email for addressee in mailing.addressees.all()]

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
                status="success", response=response, mailing=mailing
            )
            MailingService.update_status(
                mailing=mailing,
                start_at=start_at,
                completed_at=completed_at,
            )
        finally:
            return redirect(reverse("sender:mailings_list"))

    @staticmethod
    def try_to_send(status, response, mailing):
        attempt = SendTry.objects.create(
            try_at=timezone.now(),
            status=status,
            response=response,
            mailing=mailing
        )
        attempt.save()

    @staticmethod
    def update_status(mailing, start_at, completed_at):
        mailing.start_at = timezone.localtime(start_at)
        mailing.completed_at = timezone.localtime(completed_at)
        mailing.status = "completed"
        mailing.save()

    @staticmethod
    def caching(queryset, model, user=None):
        if not CACHE_ENABLED:
            return queryset.filter(owner=user)
        key = str(model) + "_list"
        objects = cache.get(key)
        if objects is not None:
            return objects
        objects = queryset.filter(owner=user)
        cache.set(key, objects, 60 * 1)
        return objects



