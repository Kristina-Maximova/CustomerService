from django.urls import path

from sender.apps import SenderConfig

from .views.addressee import (AddresseeListView, AddresseeCreateView, AddresseeDetailView,
                              AddresseeUpdateView, AddresseeDeleteView)
from .views.message import (MessageCreateView, MessageListView, MessageUpdateView,
                            MessageDetailView, MessageDeleteView)
from .views.mailing import (MailingListView, MailingCreateView, MailingDetailView,
                            MailingUpdateView, MailingDeleteView, SendMailing)
from .views.home import HomeView

app_name = SenderConfig.name  # 'sender'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('addressee/list/', AddresseeListView.as_view(), name='addressees_list'),
    path('addressee/new/', AddresseeCreateView.as_view(), name='addressee_create'),
    path('addressee/<int:pk>/', AddresseeDetailView.as_view(), name='addressee_detail'),
    path('addressee/update/<int:pk>/', AddresseeUpdateView.as_view(), name='addressee_update'),
    path('addressee/delete/<int:pk>/', AddresseeDeleteView.as_view(), name='addressee_delete'),

    path('message/list/', MessageListView.as_view(), name='messages_list'),
    path('message/new/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('mailing/list/', MailingListView.as_view(), name='mailings_list'),
    path('mailing/new/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('send-mailing/<int:pk>/', SendMailing.as_view(), name='send_mailing'),
]
