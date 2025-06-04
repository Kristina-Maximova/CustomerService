from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
from .views import ProfileUpdateView, RegisterView, email_verification

app_name = UsersConfig.name


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='sender:home'), name='logout'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),

]
