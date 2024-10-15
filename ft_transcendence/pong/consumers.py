import json

from channels.generic.websocket import AsyncWebsocketConsumer


class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.room_id = None

        # self.room_id = self.scope.get("room_id")
        # self.room_group_name = f"pong_{self.room_id}"

        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        await self.accept()

        print("Instance attributes using __dict__:")
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")

        print("All attributes in channel_layer:")
        for attr, value in self.channel_layer.__dict__.items():
            print(f"{attr}: {value}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"text_data_json: {text_data_json}")
        type = text_data_json["type"]

        if type == "join_room":
            self.room_id = text_data_json["room_id"]
            self.room_group_name = f"pong_{self.room_id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.send(
                text_data=json.dumps({"message": f"Joined room: {self.room_id}"})
            )
