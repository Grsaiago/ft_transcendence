import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

# from .game import PongGame


class PongPlayerConsumer(AsyncWebsocketConsumer):
    # para connectar por enquanto, precisa estar logado, a adição ao grupo esta sendo feita no receive com a mensagem onopen
    # dessa forma o usuário só entra no grupo quando ele envia a mensagem de join_room e não pela url
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.room_id = None
            self.room_group_name = None
            self.game_data = {}

        # self.room_id = self.scope.get("room_id")
        # self.room_group_name = f"pong_{self.room_id}"

        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        await self.accept()

        # print("Instance attributes using __dict__:")
        # for attr, value in self.__dict__.items():
        #     print(f"{attr}: {value}")

        # print("All attributes in channel_layer:")
        # for attr, value in self.channel_layer.__dict__.items():
        #     print(f"{attr}: {value}")

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

        # game = cache.get(f"{self.room_group_name}_game")

        # if game:
        #     game.stop_game()
        #     game.reset_game()
        #     cache.set(f"{self.room_group_name}_game", game)

        # # por enquanto está deletando quando o usuário desconecta, o que pode deixar o outro jogador sem saber que o outro saiu
        # # print("deleting from cache")
        # cache.delete(f"{self.room_group_name}_game")

    async def receive(self, text_data):
        # processa mensagem recebida do cliente
        text_data_json = json.loads(text_data)
        # print(f"text_data_json: {text_data_json}")
        type = text_data_json["type"]

        if type == "join_room":
            await self.add_to_group(text_data_json["room_id"])
            await self.initialize_game_data(
                text_data_json["width"], text_data_json["height"]
            )
            # await self.assign_player()
            await self.worker_initialize_game()
            # cache.set(f"{self.room_group_name}_game", self.game)

            # if not self.game.started:
            #     print("Starting worker")
        if type == "start_game":
            await self.worker_start_game()

        if type == "keydown":
            await self.update_paddles_position(text_data_json["key"], True)

        if type == "keyup":
            await self.update_paddles_position(text_data_json["key"], False)

    async def add_to_group(self, room_id):
        self.room_id = room_id
        self.room_group_name = f"pong_{self.room_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def initialize_game_data(self, width, height):
        # verifica se já existe dados do jogo em andamento se não cria um novo
        if not self.game_data:
            self.game_data = cache.get(f"{self.room_group_name}_game_data", {})

        self.game_data["width"] = width
        self.game_data["height"] = height

        cache.set(f"{self.room_group_name}_game_data", self.game_data)

    # async def assign_player(self):
    #     # adiciona o jogador ao jogo
    #     self.game_data.add_player(self.scope["user"].id, self.scope["user"].username)

    async def worker_initialize_game(self):
        # enviar mensagem ao worker para instanciar o jogo e retornar o estado inicial
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "initialize_game",
                "room_id": self.room_id,
                "room_group_name": self.room_group_name,
                "width": self.game_data["width"],
                "height": self.game_data["height"],
            },
        )

    # async def send_game_state(self, event):
    #     # envia o estado do jogo atualizado para o cliente
    #     game_state = event["game_state"]
    #     message = {"type": "update_game_state", "game_state": game_state}
    #     await self.send(text_data=json.dumps(message))

    async def worker_start_game(self):
        # inicia o jogo e envia uma tarefa para o worker processar o estado do jogo
        # self.game_data.start_game()
        # cache.set(f"{self.room_group_name}_game", self.game_data)

        # envia a tarefa para o worker
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "update_game_state",
                "room_id": self.room_id,
                "room_group_name": self.room_group_name,
            },
        )

    async def update_paddles_position(self, key, state):
        # envia mensagem para o worker
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "update_paddles_position",
                "room_id": self.room_id,
                "room_group_name": self.room_group_name,
                "key": key,
                "state": state,
            },
        )

    async def send_game_state(self, event):
        # Recebe o estado inicial do jogo enviado pelo worker
        game_state = event["game_state"]

        # Envia o estado inicial do jogo para o cliente WebSocket
        await self.send(
            text_data=json.dumps({"type": "game_init", "game_state": game_state})
        )
