from django.urls import path

from .db_paths import (
    accept_friend_request,
    block_user,
    unblock_user,
    cancel_friend_request,
    refuse_friend_request,
    remove_friendship,
    send_friend_request,
    update_user,
    get_user_friends,
    get_all_users,
    get_user_details,
    change_password,
    sign_in,
    sign_up
)

app_name = "db-user_management"

urlpatterns = [
    path("send-friend-request/", send_friend_request, name="send_friend_request"),
    path("cancel-friend-request/", cancel_friend_request, name="cancel_friend_request"),
    path("accept-friend-request/", accept_friend_request, name="accept_friend_request"),
    path("refuse-friend-request/", refuse_friend_request, name="refuse_friend_request"),
    path("remove-friendship/", remove_friendship, name="remove_friendship"),
    path("update_user/", update_user, name="update_user"),
    path("change-password/", change_password, name="change_password"),
    path("block-user/", block_user, name="block_user"),
    path("unblock-user/", unblock_user, name="unblock_user"),
    path("user/friends/", get_user_friends, name="get_user_friends"),
    path("user/", get_all_users, name="get_all_users"),
    path("user/<int:user_id>/", get_user_details, name="get_user_details"),
    path("sign-in/", sign_in, name="sign_in"),
    path("sign-up/", sign_up, name="sign_up"),
]
