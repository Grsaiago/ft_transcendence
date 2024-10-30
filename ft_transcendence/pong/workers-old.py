# # import asyncio

# from channels.consumer import AsyncConsumer
# from django.core.cache import cache


# class PongGameWorker(AsyncConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.game = None

#     async def init_game(self, room_group_name):
#         self.game = cache.get(f"{room_group_name}_game")
#         if not self.game:
#             raise Exception("Game not found in cache")

#     async def update_game_state(self, message):
#         room_group_name = message["room_group_name"]

#         if not self.game:
#             await self.init_game(room_group_name)

#         if self.game and self.game.started:
#             # atualiza o estado do jogo
#             self.game.game_loop()

#             # cache.set(f"{room_group_name}_game", self.game)

#             # envia o estado atualizado para o grupo de websockets
#             # ver de só mandar o estado da bola
#             await self.channel_layer.group_send(
#                 room_group_name,
#                 {
#                     "type": "send_game_state",
#                     "game_state": self.game.get_game_state(),
#                 },
#             )

#             # pequena pausa para simular a velocidade do jogo (60fps)
#             # await asyncio.sleep(0.008)

#             # reenvia a tarefa para si mesmo para continuar processando o estado do jogo
#             await self.channel_layer.send(
#                 "pong_update_channel",
#                 {
#                     "type": "update_game_state",
#                     "room_group_name": room_group_name,
#                 },
#             )

#     async def update_paddles_position(self, message):
#         # room_group_name = message["room_group_name"]
#         key = message["key"]
#         state = message["state"]

#         if state:
#             self.game.paddle_on(key)
#         else:
#             self.game.paddle_off(key)

#         # # envia o estado atualizado para o grupo de websockets
#         # await self.channel_layer.group_send(
#         #     room_group_name,
#         #     {
#         #         "type": "send_game_state",
#         #         "game_state": self.game.get_game_state(),
#         #     },
#         # )
