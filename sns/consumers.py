
#from channels.generic.websocket import WebsocketConsumer

#from asgiref.sync import async_to_sync  # async_to_sync() : 非同期関数を同期的に実行する際に使用する。
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection
from django.db.utils import OperationalError
from channels.db import database_sync_to_async
from django.core import serializers
from django.utils import timezone
import json
from .models import *
from urllib.parse import urlparse
import datetime
import time
# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class ChatConsumer( AsyncWebsocketConsumer ):
    groups = ['broadcast']

    async def connect(self):
        try:
            
            self.room_pk = self.scope['url_route']['kwargs']['room_pk']
            self.room_group_name = 'chat_%s' % self.room_pk
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            raise

    # WebSocket切断時の処理
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive(self, text_data):
        try:
            print(str(text_data))
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            name = text_data_json['name']
            await self.createMessage(text_data_json)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                }
            )
        except Exception as e:
            raise
    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def chat_message(self, event):
        try:
            message = event['message']
            name = event['name']
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'name': name,
            }))
        except Exception as e:
            raise
    @database_sync_to_async
    def createMessage(self, event):
        try:
            owner = User.objects.get(
                name=event['name']
            )
            room=TalkRoom.objects.get(id=int(self.room_pk))
            friend=Friend.objects.get(room=room,inviter=owner)
            receiver=friend.invitee
            new_friend_message=FriendMessage()
            new_friend_message.owner=owner
            new_friend_message.receiver=receiver
            new_friend_message.room=room
            new_friend_message.content=event['message']
            new_friend_message.save()                
        except Exception as e:
            raise 

class GroupChatConsumer( AsyncWebsocketConsumer ):
    groups = ['broadcast']

    async def connect(self):
        try:
            
            self.room_pk = self.scope['url_route']['kwargs']['room_pk']
            self.room_group_name = 'chat_%s' % self.room_pk
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            raise

    # WebSocket切断時の処理
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()
    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive(self, text_data):
        try:
            print(str(text_data))
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            name = text_data_json['name']
            await self.createMessage(text_data_json)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                }
            )
        except Exception as e:
            raise
    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def chat_message(self, event):
        try:
            message = event['message']
            name = event['name']
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'name': name,
            }))
        except Exception as e:
            raise
    @database_sync_to_async
    def createMessage(self, event):
        try:
            owner = User.objects.get(
                name=event['name']
            )
            room=TalkRoom.objects.get(id=int(self.room_pk))
            group=Group.objects.get(room=room)
            new_group_message=GroupMessage()
            new_group_message.owner=owner
            new_group_message.Group=group
            new_group_message.content=event['message']
            new_group_message.save()                
        except Exception as e:
            raise 