from django.urls import path
from .db_paths import *

app_name = "db-user_management"

urlpatterns = [
    path('send-friend-request/', send_friend_request, name="send_friend_request" ),
    path('accept-friend-request/', accept_friend_request, name="accept_friend_request"),
]
