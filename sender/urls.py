from django.urls import path

from sender.apps import SenderConfig

from .views import (AddresseeCreateView, AddresseeDetailView, AddresseeUpdateView,
                    AddresseeDeleteView, AddresseeListView,
                    MessageCreateView, MessageListView, MessageUpdateView,
                    MessageDetailView, MessageDeleteView,

                    home_view)

app_name = SenderConfig.name  # 'sender'

urlpatterns = [
    path('', home_view, name='home'),

    path('addressee/list/', AddresseeListView.as_view(), name='addressees_list'),
    path('addressee/new/', AddresseeCreateView.as_view(), name='addressee_create'),
    path('addressee/<int:pk>/', AddresseeDetailView.as_view(), name='addressee_detail'),
    path('addressee/update/<int:pk>/', AddresseeUpdateView.as_view(), name='addressee_update'),
    path('addressee/delete/<int:pk>/', AddresseeDeleteView.as_view(), name='addressee_delete'),

    path('message/list/', MessageListView.as_view(), name='messages_list'),
    path('message/new/',MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

]
