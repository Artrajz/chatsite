import datetime
import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from chat01.models import message, group_list, group
from django.contrib.auth.models import User

User = get_user_model()

connectors = {}


class ChatConsumers(WebsocketConsumer):
    # *args, **kwargs 前者叫位置参数，后者叫关键字参数
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.channel = None
        self.user_id = None

        self.groups = {}

    # 进行websocket连接
    def connect(self):
        # 获取群组ID
        self.channel = self.scope["url_route"]["kwargs"]["channel"]

        # 获取用户名，需要字符串化，原本是channels.auth.UserLazyObject类型
        self.user = str(self.scope["user"])

        # 获取用户id
        self.user_id = str(User.objects.get(username=self.user).id)

        # 映射用户id和socket通道
        connectors[self.user_id] = self.channel
        self.groups = {}

        object_group_list = group_list.objects.all().filter()
        # 获取群组用户信息
        for item in object_group_list:
            object_group = group.objects.filter(group_id_id=item.group_id)
            self.groups[str(item.group_id)] = []
            for i in object_group:
                self.groups[str(item.group_id)].append(str(i.user_id))

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
        # data={"message":,"talker":,}
        data = json.loads(text_data)

        # 获取接受方的id
        talker = data.get("talker")

        # username发送用户，message发送信息,talker接收对象
        msg = {"user_id": data["user_id"], "username": self.user, "message": data["message"],
               "talker_type": str(data["talker_type"]),"talker":talker}
        msg["success"] = "201"  # 成功接收

        # 如果接受对象是联系人
        if str(data["talker_type"]) == "1":
            # 检测接收信息的用户是否在线，若在线就发送信息
            if connectors.get(data.get("talker")) and connectors.get(data.get("talker")) != "":
                async_to_sync(self.channel_layer.group_send)(
                    connectors[talker], {"type": "chat.message", "message": msg}
                )
        elif str(data["talker_type"]) == "2":
            for i in self.groups[data.get("talker")]:
                # 检测接收信息的用户是否在线，若在线就发送信息
                if i != self.user_id:
                    if connectors.get(i) and connectors.get(i) != "":
                        async_to_sync(self.channel_layer.group_send)(
                            connectors.get(i), {"type": "chat.message", "message": msg}
                        )

        msg["success"] = "200"  # 成功发送
        async_to_sync(self.channel_layer.group_send)(
            connectors[self.user_id], {"type": "chat.message", "message": msg}
        )

        # user_id_id = User.objects.get(username=self.user).id
        # talker_type = data["talker_type"]
        # talker_id = talker
        # create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # content = data["message"]
        #
        # print(user_id_id,talker_type,talker_id,create_time,content)

        # 消息存入数据库
        db_message = message(
            user_id_id=self.user_id,
            talker_type=data["talker_type"],
            talker_id_id=talker,
            create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            content=data["message"],
        )
        db_message.save()

    # channel_layer用来发送消息的函数
    def chat_message(self, event):
        self.send(text_data=json.dumps(event["message"]))
