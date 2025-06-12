from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import MailUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = 'testmanager@sender.com'
        password = '123456Tm'
        user = MailUser.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        user.is_staff = False
        managers_group, created = Group.objects.get_or_create(name="Managers")
        # Получаем разрешения
        can_view_all_addressees = Permission.objects.get(codename='can_view_all_addressees')
        can_view_all_messages = Permission.objects.get(codename='can_view_all_messages')
        can_view_all_mailings = Permission.objects.get(codename='can_view_all_mailings')
        can_block_users = Permission.objects.get(codename='can_block_users')
        can_stop_mailing = Permission.objects.get(codename='can_stop_mailing')
        # Назначаем разрешения группе
        managers_group.permissions.add(can_view_all_addressees,
                                       can_view_all_messages,
                                       can_view_all_mailings,
                                       can_block_users,
                                       can_stop_mailing,
                                       )
        managers_group.save()

        user.groups.add(managers_group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'''Пользователь добавлен в группу "Managers"
                email: {email}
                пароль: {password}'''
            )
        )
