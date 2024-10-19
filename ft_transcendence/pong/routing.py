from django.urls import path

from .consumers import PongPlayerConsumer

ws_pong_application = [path("ws/pong/", PongPlayerConsumer.as_asgi())]
