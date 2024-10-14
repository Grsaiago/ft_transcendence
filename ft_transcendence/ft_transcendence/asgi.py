"""
ASGI config for transcendence project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from pong.routing import ws_pong_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_transcendence.settings")
# A gente inicializa as configs do Django antes pra ele carregar
# as models caso a gente as use em algum consumer (a gente usa xD).
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns + ws_pong_application))
        ),
    }
)
