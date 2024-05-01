import json
from datetime import datetime 
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    user_count = 0 

    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(self.roomGroupName, self.channel_name)

        await self.accept() 

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.roomGroupName, self.channel_name)


    async def receive(self, text_data):
        # parse the incoming JSON data
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username", "Anonymous")

        # get the current time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format as a string

        # send the message to the group with the time
        await self.channel_layer.group_send(
            self.roomGroupName,
            {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "timestamp": timestamp,  
            }
        )

    async def sendMessage(self, event):
        # send the message to the WebSocket client with the time
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"] 

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "timestamp": timestamp, 
        }))
  
