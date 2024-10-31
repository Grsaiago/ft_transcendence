import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

# from .game import PongGame


class PongPlayerConsumer(AsyncWebsocketConsumer):
    # para connectar por enquanto, precisa estar logado, a adição ao grupo esta sendo feita no receive com a mensagem vinda de onopen
    # dessa forma o usuário só entra no grupo quando ele envia a mensagem de join_room e não pela url
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.room_id = None
            self.room_group_name = None
            self.game_data = {}

        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            # envia mensagem para o worker para finalizar o jogo
            await self.channel_layer.send(
                "pong_update_channel",
                {
                    "type": "finish_game",
                    "room_id": str(self.room_id),
                },
            )
            # remove o usuário do grupo
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        # processa mensagem recebida do cliente
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]

        if type == "join_room":
            await self.add_to_group(text_data_json["room_id"])
            await self.initialize_game_data(
                text_data_json["width"], text_data_json["height"]
            )
            await self.worker_initialize_game()

        if type == "start_game":
            await self.worker_start_game()

        if type == "keydown":
            await self.worker_update_paddles_position(text_data_json["key"], True)

        if type == "keyup":
            await self.worker_update_paddles_position(text_data_json["key"], False)

    async def add_to_group(self, room_id):
        self.room_id = room_id
        self.room_group_name = f"pong_{self.room_id}"
        self.game_data = cache.get(f"{self.room_group_name}_game_data", {})
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def initialize_game_data(self, width, height):
        # verifica se já existe dados do jogo em andamento se não cria um novo
        if not self.game_data:
            self.game_data["width"] = width
            self.game_data["height"] = height
            cache.set(f"{self.room_group_name}_game_data", self.game_data)

        # adicionar dados necessários para o jogo, como os jogadores?

    async def worker_initialize_game(self):
        # enviar mensagem ao worker para instanciar o jogo e retornar o estado inicial para desenhar na tela
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "initialize_game",
                "room_id": str(self.room_id),
                "room_group_name": self.room_group_name,
                "width": self.game_data["width"],
                "height": self.game_data["height"],
            },
        )

    async def worker_start_game(self):
        # envia mensagem para o worker para atualizar o estado do jogo, no caso, começar o loop
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "update_game_state",
                "room_id": str(self.room_id),
                "room_group_name": self.room_group_name,
            },
        )

    async def worker_update_paddles_position(self, key, state):
        # envia mensagem para o worker e atualiza as variáveis dos paddles
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "update_paddles_position",
                "room_id": str(self.room_id),
                "key": key,
                "state": state,
            },
        )

    async def send_game_state(self, event):
        # Recebe o estado do worker
        game_state = event["game_state"]

        # Envia o estado do jogo para o cliente WebSocket
        await self.send(
            text_data=json.dumps({"type": "game_init", "game_state": game_state})
        )
