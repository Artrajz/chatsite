from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 服务端与客户端创建连接
        self.accept()

        # 获取群号
        self.group = self.scope['url_route']['kwargs'].get('group')

        # 将异步转换成同步，加入连接对象
        async_to_sync(self.channel_layer.group_add(self.group, self.channel_name))

    def websocket_receive(self, message):
        # 通知group内的所有客户端，执行type方法，type方法可以自己定义
        async_to_sync(self.channel_layer.group_send)(self.group, {"type": "chat_messages", "message": message})

    def chat_messages(self, event):
        print(event)
        text = event["message"]["text"]
        self.send(text)


    def websocket_disconnect(self, message):
        # 断开连接时移除连接对象
        async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)
        raise StopConsumer()
