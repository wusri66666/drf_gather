from django.urls import path
from app.consumers import ChatConsumer, AsyncChatConsumer


websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer),
    path('ws/async_chat/', AsyncChatConsumer),
]