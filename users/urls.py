from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
from .services import block_user, email_verification
from .views import (EmailConfirmationView,
                    ProfileUpdateView,
                    PasswordRecoveryView,
                    UserCreateView,
                    UserDeleteView,
                    UserDetailView,
                    UserListView,
                    UserLoginView,
                    UserUpdateView, )

app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", LogoutView.as_view(next_page='sender:home'), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="users"),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path(
        "email-confirmation/",
        EmailConfirmationView.as_view(),
        name="email_confirmation",
    ),
    path("password-recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
    path("block_user/<int:pk>", block_user, name="block_user"),
]

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
#     path('logout/', LogoutView.as_view(next_page='sender:home'), name='logout'),
#     path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
#     path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
# ]
