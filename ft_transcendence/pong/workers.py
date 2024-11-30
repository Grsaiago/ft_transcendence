import asyncio

from channels.consumer import AsyncConsumer

from .game import PongGame

# from django.core.cache import cache


class PongGameWorker(AsyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = {}  # Dicionários para armazenar instâncias dos jogos
        self.tasks = {}  # Dicionários para armazenar tarefas de cada jogo

    async def initialize_game(self, message):
        room_id = message["room_id"]
        room_group_name = message["room_group_name"]
        width = message["width"]
        height = message["height"]

        # print("games: ", self.game)
        # print("tasks: ", self.game)

        if room_id not in self.game:
            self.game[room_id] = PongGame(width, height)

        game_state = await self.game[room_id].get_game_state()

        await self.channel_layer.group_send(
            room_group_name,
            {
                "type": "send_game_state",
                "game_state": game_state,
            },
        )

    async def start_game_loop(self, room_id, room_group_name):
        while room_id in self.game:
            game_state = await self.game[room_id].calculate_game_tick()
            print("game_state: ", game_state)
            # enviar as informações do jogo para o grupo de websockets
            await self.channel_layer.group_send(
                room_group_name,
                {
                    "type": "send_game_state",
                    "game_state": game_state,
                },
            )

            if self.game[room_id].has_winner():
                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        "type": "send_winner",
                        "game_state": game_state,
                    },
                )
                del self.game[room_id]
                if self.tasks[room_id]:
                    self.tasks[room_id].cancel()
                    del self.tasks[room_id]

            # pequena pausa para simular a velocidade do jogo (60fps)
            await asyncio.sleep(0.016)

    async def update_game_state(self, message):
        room_id = message["room_id"]
        room_group_name = message["room_group_name"]

        # Inicializa o jogo se ainda não foi inicializado
        if room_id not in self.game:
            await self.initialize_game(message)

        # Inicia a tarefa de loop do jogo se ainda não foi iniciada
        if room_id not in self.tasks:
            self.tasks[room_id] = asyncio.create_task(
                self.start_game_loop(room_id, room_group_name)
            )

    async def update_paddles_position(self, message):
        room_id = message["room_id"]
        paddle = message["paddle"]
        direction = message["direction"]
        state = message["state"]

        if room_id in self.game:
            if state:
                await self.game[room_id].paddle_on(paddle, direction)
            else:
                await self.game[room_id].paddle_off(paddle)

    async def finish_game(self, message):
        room_id = message["room_id"]
        if room_id in self.game:
            del self.game[room_id]
            if room_id in self.tasks:
                self.tasks[room_id].cancel()
                del self.tasks[room_id]


#############
# without async

# class PongGameWorker(AsyncConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.game = {}  # Dicionários para armazenar instâncias

#     async def initialize_game(self, message):
#         room_id = message["room_id"]
#         room_group_name = message["room_group_name"]
#         width = message["width"]
#         height = message["height"]

#         if room_id not in self.game:
#             self.game[room_id] = PongGame(width, height)

#         game_state = await self.game[room_id].get_game_state()

#         await self.channel_layer.group_send(
#             room_group_name,
#             {
#                 "type": "send_game_state",
#                 "game_state": game_state,
#             },
#         )

#     async def update_game_state(self, message):
#         room_id = message["room_id"]
#         room_group_name = message["room_group_name"]

#         if room_id not in self.game:
#             await self.initialize_game(message)

#         await self.game[room_id].game_loop()
#         game_state = await self.game[room_id].get_game_state()

#         await self.channel_layer.group_send(
#             room_group_name,
#             {
#                 "type": "send_game_state",
#                 "game_state": game_state,
#             },
#         )

#         # pequena pausa para simular a velocidade do jogo (60fps)
#         await asyncio.sleep(0.016)

#         # reenvia a tarefa para si mesmo para continuar processando o estado do jogo
#         await self.channel_layer.send(
#             "pong_update_channel",
#             {
#                 "type": "update_game_state",
#                 "room_id": room_id,
#                 "room_group_name": room_group_name,
#             },
#         )

#     async def update_paddles_position(self, message):
#         room_id = message["room_id"]
#         # room_group_name = message["room_group_name"]
#         key = message["key"]
#         state = message["state"]

#         if state:
#             await self.game[room_id].paddle_on(key)
#         else:
#             await self.game[room_id].paddle_off(key)

#         # # envia o estado atualizado para o grupo de websockets
#         # await self.channel_layer.group_send(
#         #     room_group_name,
#         #     {
#         #         "type": "send_game_state",
#         #         "game_state": self.game.get_game_state(),
#         #     },
#         # )
