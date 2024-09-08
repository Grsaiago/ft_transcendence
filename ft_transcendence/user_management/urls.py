from django.urls import path

from .views import (
    UserChangePasswordView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
)

app_name = "user_management"

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="register"),
    path("login", UserLoginView.as_view(), name="login"),
    path("logout", UserLogoutView.as_view(), name="logout"),
    path("change_password", UserChangePasswordView.as_view(), name="change_password"),
]
