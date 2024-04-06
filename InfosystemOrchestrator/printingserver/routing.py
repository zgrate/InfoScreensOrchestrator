from django.urls import re_path

from printingserver import consumers

websocket_urlpatterns = [
    re_path(r"ws/printingservice/", consumers.PrintingServiceWebsocket.as_asgi()),
]