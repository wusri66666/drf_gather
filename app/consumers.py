from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.http import QueryDict

PENDING = {}


class Agent:
    def __init__(self, client, group):
        self.agent = client
        group = PENDING.setdefault(group, [])
        group.append(self.agent)

    @classmethod
    async def send_data(cls, client, data):
        await client.send(data)


# 同步实现方式一：自定义封装存储consumer
class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        group = QueryDict(bytes.decode(self.scope.get("query_string"))).get('id')
        Agent(self, group)

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        print(text_data)

    def disconnect(self, close_code):
        self.close()
        group = QueryDict(bytes.decode(self.scope.get("query_string"))).get('id')
        PENDING.get(group).remove(self)


# 同步实现方式二：利用CHANNEL_LAYERS存储consumer
# class ChatConsumer(JsonWebsocketConsumer):
#     def get_groups(self):
#         return [QueryDict(bytes.decode(self.scope.get("query_string"))).get('id')]
#
#     def websocket_connect(self, message):
#         self.groups = self.get_groups()
#         super(ChatConsumer, self).websocket_connect(message)
#
#     @classmethod
#     def group_send(cls, group, content, close=False):
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             group, {
#                 "type": "group.message",
#                 "content": content,
#                 "close": close
#             })
#
#     def group_message(self, message):
#         self.send(text_data=message["content"], close=message["close"])
#
#     def receive(self, text_data=None, bytes_data=None, **kwargs):
#         print(text_data)


# 异步实现方式一：自定义封装存储consumer
class AsyncChatConsumer(AsyncJsonWebsocketConsumer):
    def get_group(self):
        group = QueryDict(bytes.decode(self.scope.get("query_string"))).get('id')
        return group

    async def websocket_connect(self, message):
        await self.accept()
        group = self.get_group()
        Agent(self, group)

    async def websocket_receive(self, message):
        data = message.get('text')
        group = self.get_group()
        for client in PENDING.get(group):
            await Agent.send_data(client, data)

    async def websocket_disconnect(self, message):
        await self.close()
        group = QueryDict(bytes.decode(self.scope.get("query_string"))).get('id')
        PENDING.get(group).remove(self)
