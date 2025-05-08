from django.urls import path

from sender.apps import SenderConfig

from .views import (AddresseeCreateView,
                    AddresseeDetailView,
                    AddresseeUpdateView,
                    AddresseeDeleteView,

                    home_view)

app_name = SenderConfig.name  # 'sender'

urlpatterns = [
    path('', home_view, name='home'),
    path('addressee/new', AddresseeCreateView.as_view(), name='addressee_create'),
    path('addressee/<int:pk>/', AddresseeDetailView.as_view(), name='addressee_detail'),
    path('addressee/update/<int:pk>/', AddresseeUpdateView.as_view(), name='addressee_update'),
    path('addressee/delete/<int:pk>/', AddresseeDeleteView.as_view(), name='addressee_delete'),

]
