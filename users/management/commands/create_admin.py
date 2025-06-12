from django.core.management.base import BaseCommand

from users.models import MailUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = MailUser.objects.create(email='testadmin@testadmin.com')
        user.set_password('123456Ta')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Успешно создан admin с почтой {user.email}'))
