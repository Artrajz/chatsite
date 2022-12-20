from django.urls import re_path
from chat01 import consumers

websocket_urlpatterns = {
    re_path(r'group/(?P<group>\w+)/$', consumers.ChatConsumers.as_asgi()),
    re_path(r'contact/(?P<contact>\w+)/$', consumers.ChatConsumer.as_asgi()),
}
