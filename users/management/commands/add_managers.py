from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import MailUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Group.objects.filter(name='Managers').exists():
            Group.objects.filter(name='Managers').delete()
        managers_group = Group.objects.create(name='Managers')
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
        # Cоздаем пользователей
        manager_1 = MailUser.objects.create(email='athos@sender.com')
        manager_1.set_password('Athos1')
        manager_1.is_active = True
        manager_1.is_staff = False
        pass_1 = 'Athos1'

        manager_2 = MailUser.objects.create(email='porthos@sender.com')
        manager_2.set_password('Porthos2')
        manager_2.is_active = True
        manager_2.is_staff = False
        pass_2 = 'Porthos2'

        manager_3 = MailUser.objects.create(email='aramis@sender.com')
        manager_3.set_password('Aramis3')
        manager_3.is_active = True
        manager_3.is_staff = False
        pass_3 = 'Aramis3'

        # Добавляем пользователей в группу
        manager_1.groups.add(managers_group)
        manager_2.groups.add(managers_group)
        manager_3.groups.add(managers_group)
        # Сохраняем пользователей
        manager_1.save()
        manager_2.save()
        manager_3.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'''D группу "Managers" добавлены:
                {manager_1.email} c паролем {pass_1}
                {manager_2.email} c паролем {pass_2}
                {manager_3.email} c паролем {pass_3}'''
            )
        )
