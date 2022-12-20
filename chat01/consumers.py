import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumers(WebsocketConsumer):
    # *args, **kwargs 前者叫位置参数，后者叫关键字参数
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    # 进行websocket连接
    def connect(self):
        # 获取群组ID
        self.room_group_name = self.scope["url_route"]["kwargs"]["group"]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # 接受连接
        self.accept()

    # 断开websocket连接
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        raise StopConsumer

    # 接收websocket的消息
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": text_data}
        )

    # channel_layer用来发送消息的函数
    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"]}))


class Clients:
    pass


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # Make a database row with our channel name
        Clients.objects.create(channel_name=self.channel_name)

    def disconnect(self, close_code):
        # Note that in some rare cases (power loss, etc) disconnect may fail
        # to run; this naive example would leave zombie channel names around.
        Clients.objects.filter(channel_name=self.channel_name).delete()

    def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        self.send(text_data=event["text"])
