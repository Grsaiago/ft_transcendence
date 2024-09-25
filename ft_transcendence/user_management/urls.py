from django.urls import path

from .views import (
    UserChangePasswordView,
    UserFriendListView,
    UserSignInView,
    UserLogoutView,
    UserSignUpView,
    HomepageView,
    UserProfileView,
)

app_name = "user_management"

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("sign_up/", UserSignUpView.as_view(), name="sign_up"),
    path("sign_in/", UserSignInView.as_view(), name="sign_in"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("change_password/", UserChangePasswordView.as_view(), name="change_password"),
    path("friend_list/", UserFriendListView.as_view(), name="friend_list"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
