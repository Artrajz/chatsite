from django.urls import re_path
from chat01 import consumers

websocket_urlpatterns = {
    re_path(r'channel/(?P<channel>\w+)/$', consumers.ChatConsumers.as_asgi()),
}
