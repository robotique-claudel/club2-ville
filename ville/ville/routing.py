from ville.consumers import objetConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter(
    {
       "websocket": AuthMiddlewareStack(
        URLRouter([
            url("", objetConsumer),
        ])
        ),
    }
)
