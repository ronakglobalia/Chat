
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from chat import views as chat_views


urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),
    path("room/", chat_views.create_room, name="room-page"),
    path("room-list/", chat_views.room_list, name="room-list"),
    path("chat/<str:uuid>/", chat_views.chat, name="chat"),
 
    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chat/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]