import json
import base64
import io, os
from PIL import Image
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import SingleChatGroup, TextMessage, Room

    

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = str(self.scope['session'].get('group_name'))
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    @database_sync_to_async
    def get_all_messages(self, room):
        datas = []
        data = TextMessage.objects.filter(room__room_id=room).values("user", "text_data")
        for i in data:
            user = User.objects.get(id=i.get("user")).username
            texts = {"user": f"{user}", "text": f"{i.get('text_data')}"}
            datas.append(json.dumps(texts))	
        return datas

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        messages = text_data_json["message"]
        username = text_data_json["username"]
        room_id = self.scope['session'].get('group_name')

        room = await self.get_room(room_id)
        user = await self.get_user(self.scope['session'].get('username'))

        message = TextMessage(room=room, user=user, text_data=messages)
        await self.save_message(message)

        messages_list = await self.get_all_messages(room_id)

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": text_data_json['type'],
                "message": messages_list,
                "username": username,
            }
        )

    @database_sync_to_async
    def get_room(self, room_id):
        return Room.objects.get(room_id=room_id)

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def save_message(self, message):
        message.save()

    async def text(self, event):
        message = event["message"]
        username = event["username"]
        type = event["type"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "type": type}))

    async def image(self, event):
        message = event["message"]
        username = event["username"]
        type = event["type"]
        for _ in range(1):
            await self.send(text_data=json.dumps({"message": message, "username": username, "type": type}))




class StoreChatConsumer(WebsocketConsumer):
	def connect(self):
		self.roomGroupName = str(self.scope['session'].get('group_name'))
		self.channel_layer.group_add(
			self.roomGroupName,
			self.channel_name
		)
		self.accept()
	
	def get_all_messages(self, room):
		datas = []
		data = TextMessage.objects.filter(room__room_id=room).values("user", "text_data")
		for i in data:
			texts = {"user":User.objects.get(id=i.get("user")), "text":i.get("text_data")}
			datas.append(texts)
		return datas
  
	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		messages = text_data_json["message"]
		print(f"==>> message: {messages}")
		username = text_data_json["username"]
		room = Room.objects.get(room_id=self.scope['session'].get('group_name'))
		message = TextMessage()
		message.room = room
		message.user_id = User.objects.get(username=self.scope['session'].get('username')).id
		message.text_data = messages
		message.save()
		messages_list = self.get_all_messages(self.scope['session'].get('group_name'))
		print(f"==>> messages_list: {messages_list}")
		# message_type = text_data_json["message_type"]
		# if message_type == "image":
		# 	base64_string = message.split(',')[1]
		# 	image_bytes = base64.b64decode(base64_string)
		# 	image_path = os.path.join('/home/ts/Documents/Rajnish/RealTime/media', 'image.jpg')
		# 	with open(image_path, 'wb') as image_file:
		# 		image_file.write(image_bytes)

		self.channel_layer.group_send(
			self.roomGroupName,{
				"type" :  text_data_json['type'],
				"message" : messages_list ,
				"username" : username ,
			})
	def text(self , event) :
		message = event["message"]	
		print(f"==>> message============: {message}")
		username = event["username"]
		type = event["type"]
		self.send(text_data = json.dumps({"message":message ,"username":username, "type": type}))
	
	def image(self , event) :
		message = event["message"]
		username = event["username"]
		type = event["type"]
		self.send(text_data = json.dumps({"message":message ,"username":username, "type": type}))