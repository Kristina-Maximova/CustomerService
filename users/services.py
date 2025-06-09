from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import MailUser


def email_verification(request, token):
    user = get_object_or_404(MailUser, token=token)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse("users:login"))


@permission_required("users.view_user")
def block_user(self, pk):
    user = MailUser.objects.get(pk=pk)
    user.is_active = {user.is_active: False, not user.is_active: True}[True]
    user.save()
    return redirect(reverse("users:users"))
