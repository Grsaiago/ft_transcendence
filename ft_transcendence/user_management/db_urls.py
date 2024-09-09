from django.urls import path

from .db_paths import (
    accept_friend_request,
    block_user,
    cancel_friend_request,
    refuse_friend_request,
    remove_friendship,
    send_friend_request,
)

app_name = "db-user_management"

urlpatterns = [
    path("send-friend-request/", send_friend_request, name="send_friend_request"),
    path("cancel-friend-request/", cancel_friend_request, name="cancel_friend_request"),
    path("accept-friend-request/", accept_friend_request, name="accept_friend_request"),
    path("refuse-friend-request/", refuse_friend_request, name="refuse_friend_request"),
    path("remove-friendship/", remove_friendship, name="remove_friendship"),
    path("block-user/", block_user, name="block_user"),
]
