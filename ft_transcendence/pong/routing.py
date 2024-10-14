from django.urls import path

from .consumers import PongConsumer

ws_pong_application = [path("ws/pong/", PongConsumer.as_asgi())]
