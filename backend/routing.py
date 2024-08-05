from django.urls import path,re_path
from .consumers import AsyncChatConsumer

websocket_urlpatterns = [
    # path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()), 
    re_path(r"chat/(?P<room_id>\w+)$", AsyncChatConsumer.as_asgi()),
    re_path(r"chat/(?P<room_id>\w+)/$", AsyncChatConsumer.as_asgi()),

    # re_path(r"groupchat/(?P<room_id>\w+)$", AsyncGroupChatConsumer.as_asgi()),
    # re_path(r"groupchat/(?P<room_id>\w+)/$", AsyncGroupChatConsumer.as_asgi()),
] 