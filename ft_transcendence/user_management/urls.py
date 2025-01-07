from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    UserChangePasswordView,
    UserFriendListView,
    UserSignInView,
    UserLogoutView,
    UserSignUpView,
    UserProfileView,
    UserChatView,
    UserFriendsView,
    UserDetailView,
    UserUpdateInfoView,
)

app_name = "user_management"

urlpatterns = [
    path("sign_up/", UserSignUpView.as_view(), name="sign_up"),
    path("sign_in/", UserSignInView.as_view(), name="sign_in"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("change_password/", UserChangePasswordView.as_view(), name="change_password"),
    path("update_info/", UserUpdateInfoView.as_view(), name="update_info"),
    path("friend_list/", UserFriendListView.as_view(), name="friend_list"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("chat/", UserChatView.as_view(), name="chat"),
    path("friends/", UserFriendsView.as_view(), name="friends"),
    path("user/<int:user_id>/", UserDetailView.as_view(), name="user_details"),
    path("", UserProfileView.as_view(), name="homepage"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
