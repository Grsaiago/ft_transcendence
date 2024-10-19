from django.urls import path

from .consumers import PongPlayerConsumer
from .workers import PongGameWorker

ws_pong_application = [path("ws/pong/", PongPlayerConsumer.as_asgi())]

channel_routing = {
    "pong_update_channel": PongGameWorker.as_asgi(),
}
