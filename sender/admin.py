from django.contrib import admin

from .models import Addressee, Mailing, Message, SendTry


# Register your models here.
@admin.register(Addressee)
class AddresseeAdmin(admin.ModelAdmin):
    """ Администрирование получателя почты"""
    list_display = ('email', 'full_name', 'comment',)
    list_filter = ('full_name',)
    search_fields = ('email', 'full_name', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """ Администрирование почтового сообщения"""
    list_display = ('subject', 'text',)
    list_filter = ('subject',)
    search_fields = ('subject', 'text',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """ Администрирование рассылки"""
    list_display = ('status', 'start_at', 'completed_at', 'message')
    list_filter = ('status',)
    search_fields = ('status',)


@admin.register(SendTry)
class SendTryAdmin(admin.ModelAdmin):
    """ Администрирование попытки рассылки """
    list_display = ('try_at', 'status', 'response', 'mailing')
    list_filter = ('status', 'try_at',)
    search_fields = ('status',)
