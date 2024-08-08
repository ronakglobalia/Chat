from django.urls import path , include
from django.urls import re_path
from chat.consumers import ChatConsumer, StoreChatConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
	re_path("" , ChatConsumer.as_asgi()) ,
	# re_path("store/" , StoreChatConsumer.as_asgi()) ,
]
