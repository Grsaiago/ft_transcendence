from django.urls import path

from .views import (
    UserChangePasswordView,
    UserFriendListView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    HomepageView,
)

app_name = "user_management"

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("change_password/", UserChangePasswordView.as_view(), name="change_password"),
    path("friend_list/", UserFriendListView.as_view(), name="friend_list"),
]
