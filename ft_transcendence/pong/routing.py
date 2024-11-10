from django.urls import path

from .consumers.local_consumer import LocalPongConsumer
from .workers import PongGameWorker

ws_pong_application = [path("ws/pong/local/", LocalPongConsumer.as_asgi())]

channel_routing = {
    "pong_update_channel": PongGameWorker.as_asgi(),
}
