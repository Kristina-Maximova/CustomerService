from django.urls import path

from sender.apps import SenderConfig

from . import views

app_name = SenderConfig.name

urlpatterns = [
    path('', views.LetterListView.as_view(), name = 'home'),

]
