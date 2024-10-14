import json

from channels.generic.websocket import AsyncWebsocketConsumer


class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if message == "pong":
            await self.send(
                text_data=json.dumps({"message": "Hello, world from PongConsumer!"})
            )
