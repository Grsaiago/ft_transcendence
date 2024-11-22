from django.urls import path

from .consumers.local_consumer import LocalPongConsumer
from .consumers.online_consumer import OnlinePongConsumer
from .workers import PongGameWorker

ws_pong_application = [
    path("ws/pong/local/", LocalPongConsumer.as_asgi()),
    path("ws/pong/online/", OnlinePongConsumer.as_asgi()),
    # path("ws/pong/tournament/", tournamentPongConsumer.as_asgi()), #future implementation
]

channel_routing = {
    "pong_update_channel": PongGameWorker.as_asgi(),
}
