import os
from django.core.asgi import get_asgi_application


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealChat.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
	{
		"http" : django_asgi_app,
		"websocket" : AuthMiddlewareStack(
			URLRouter(
				routing.websocket_urlpatterns
			)
		)
	}
)

# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealChat.settings')
# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     # Just HTTP for now. (We can add other protocols later.)
# })