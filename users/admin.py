from django.contrib import admin

from .models import MailUser

# Register your models here.
@admin.register(MailUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', )
    search_fields = ('email',)