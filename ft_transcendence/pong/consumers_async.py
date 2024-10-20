# import asyncio
# import json

# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.core.cache import cache

# from .game import PongGame


# class PongPlayerConsumer(AsyncWebsocketConsumer):
#     # para connectar por enquanto, precisa estar logado, a adição ao grupo esta sendo feita no receive com a mensagem onopen
#     # dessa forma o usuário só entra no grupo quando ele envia a mensagem de join_room e não pela url
#     async def connect(self):
#         if self.scope["user"].is_anonymous:
#             await self.close()
#         else:
#             self.room_id = None
#             self.loop_task = None

#         # self.room_id = self.scope.get("room_id")
#         # self.room_group_name = f"pong_{self.room_id}"

#         # await self.channel_layer.group_add(
#         #     self.room_group_name,
#         #     self.channel_name
#         # )

#         await self.accept()

#         # print("Instance attributes using __dict__:")
#         # for attr, value in self.__dict__.items():
#         #     print(f"{attr}: {value}")

#         # print("All attributes in channel_layer:")
#         # for attr, value in self.channel_layer.__dict__.items():
#         #     print(f"{attr}: {value}")

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#         game = cache.get(f"{self.room_group_name}_game_state")
#         print(f"game: {game}")

#         if game:
#             print(f"Disconnecting ... Game state: {game}")
#             game.stop_game()
#             game.reset_game()
#             print(f"After reset: Ball position: {game.ball.x}, {game.ball.y}")
#             print(f"after stop: game.started: {game.started}")
#             cache.set(f"{self.room_group_name}_game_state", game)
#             # cancel the loop task
#             if self.loop_task:
#                 print("canceling loop task")
#                 self.loop_task.cancel()
#                 try:
#                     await self.loop_task
#                 except asyncio.CancelledError:
#                     print("loop task canceled successfully")

#         print("deleting from cache")
#         cache.delete(f"{self.room_group_name}_game_state")

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print(f"text_data_json: {text_data_json}")
#         type = text_data_json["type"]

#         if type == "join_room":
#             await self.add_to_group(text_data_json["room_id"])
#             game = await self.initialize_game_state(
#                 text_data_json["width"], text_data_json["height"]
#             )
#             await self.assign_player(game)
#             await self.send_game_init(game)

#             if not game.started:
#                 await self.start_game_loop(game)

#     async def add_to_group(self, room_id):
#         self.room_id = room_id
#         self.room_group_name = f"pong_{self.room_id}"
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#     async def initialize_game_state(self, width, height):
#         game = cache.get(f"{self.room_group_name}_game_state")
#         if not game:
#             game = PongGame(width, height)
#             cache.set(f"{self.room_group_name}_game_state", game)
#         return game

#     async def assign_player(self, game):
#         game.add_player(self.scope["user"].id, self.scope["user"].username)

#     async def send_game_init(self, game):
#         message = {"type": "game_init", "game_state": game.get_game_state()}
#         print(f"message: {message}")
#         await self.send(text_data=json.dumps(message))

#     async def send_game_state(self, game):
#         message = {"type": "update_game_state", "game_state": game.get_game_state()}
#         await self.send(text_data=json.dumps(message))

#     async def start_game_loop(self, game):
#         game.start_game()
#         cache.set(f"{self.room_group_name}_game_state", game)
#         # inicia o loop do jogo e salva a task para poder cancelar depois
#         self.loop_task = asyncio.create_task(self.run_game_loop(game))

#     async def run_game_loop(self, game):
#         while game.started:
#             game.game_loop()
#             cache.set(f"{self.room_group_name}_game_state", game)
#             await self.send_game_state(game)
#             await asyncio.sleep(0.01666)
