import datetime
import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from chat01.models import message
from django.contrib.auth.models import User

User = get_user_model()
connectors = {}
groups = {}

class ChatConsumers(WebsocketConsumer):
    # *args, **kwargs 前者叫位置参数，后者叫关键字参数
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.channel = None
        self.user_id = None

    # 进行websocket连接
    def connect(self):
        # 获取群组ID
        self.channel = self.scope["url_route"]["kwargs"]["channel"]

        # 获取用户名，需要字符串化，原本是channels.auth.UserLazyObject类型
        self.user = str(self.scope["user"])

        #获取用户id
        self.user_id = str(User.objects.get(username=self.user).id)

        #映射用户id和socket通道
        connectors[self.user_id] = self.channel

        async_to_sync(self.channel_layer.group_add)(
            connectors[self.user_id], self.channel_name
        )


        # 接受连接
        self.accept()

    # 断开websocket连接
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            connectors[self.user_id], self.channel_name
        )
        raise StopConsumer

    # 接收websocket的消息
    def receive(self, text_data):
        #data={"message":,"talker":,}
        data = json.loads(text_data)

        talker = data.get("talker")

        #username发送用户，message发送信息,talker接收对象
        msg = {"username": self.user,"message":data["message"]}

        #检测接收信息的用户是否在线，若在线就发送信息
        if connectors.get(data.get("talker")) and connectors.get(data.get("talker")) != "":
            async_to_sync(self.channel_layer.group_send)(
                connectors[talker], {"type": "chat.message", "message": msg}
            )

        # user_id = User.objects.get(username=self.user).id
        # talker_type = data["talker_type"]
        # talker_id = talker
        # create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # content = data["message"]
        #
        # print(user_id,talker_type,talker_id,create_time,content)

        #消息存入数据库
        db_message = message(
            user_id = self.user_id,
            talker_type = data["talker_type"],
            talker_id_id = talker,
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            content = data["message"],
        )
        db_message.save()

    # channel_layer用来发送消息的函数
    def chat_message(self, event):
        self.send(text_data=json.dumps(event["message"]))

