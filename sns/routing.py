from django.urls import include, path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.urls import path
from sns.consumers import *

websocket_urlpatterns = [
    path( 'ws/<str:room_pk>', ChatConsumer.as_asgi() ),
    path('ws/group/<str:room_pk>',GroupChatConsumer.as_asgi())
]
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})