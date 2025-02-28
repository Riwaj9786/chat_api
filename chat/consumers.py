import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async, sync_to_async
from django.contrib.auth.models import AnonymousUser

from accounts.models import User
from chat.models import ChatRoom, Message


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f"chat_{self.room_slug}"

        user = self.scope["user"]

        self.chat_room = await self.get_chat_room(self.room_slug)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        if user.is_authenticated:
            if self.chat_room and user in await self.get_chat_room_users():
                await self.accept()
                print(f"Connection Established for {self.room_slug}...")

            else:
                print("You are not in the ChatRoom!")
                await self.close()
        else:
            print("You are not authenticated!")
            await self.close()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"WebSocket Disconnected from {self.room_slug} with code {close_code}...")


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_text = data.get('message')
            user = self.scope['user']

            if user.is_anonymous:
                await self.send(text_data=json.dumps({"error": "User not authenticated!"}))
                return 
            
            message = await self.create_message(self.chat_room, user, message_text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_text,
                    "sender": user.email,
                    "timestamp": str(message.created_at),
                },
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format."}))


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))

    @database_sync_to_async
    def get_chat_room(self, slug):
        return ChatRoom.objects.filter(slug=slug).first()

    @database_sync_to_async
    def get_user(self, id):
        return User.objects.filter(id=id).first()

    @database_sync_to_async
    def create_message(self, room, sender, message):
        return Message.objects.create(room=room, sender=sender, message=message)
    
    @sync_to_async
    def get_chat_room_users(self):
        return list(self.chat_room.members.all())
