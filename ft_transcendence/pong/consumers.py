import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from .game import PongGame


class PongPlayerConsumer(AsyncWebsocketConsumer):
    # para connectar por enquanto, precisa estar logado, a adição ao grupo esta sendo feita no receive com a mensagem onopen
    # dessa forma o usuário só entra no grupo quando ele envia a mensagem de join_room e não pela url
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

        # print("Instance attributes using __dict__:")
        # for attr, value in self.__dict__.items():
        #     print(f"{attr}: {value}")

        # print("All attributes in channel_layer:")
        # for attr, value in self.channel_layer.__dict__.items():
        #     print(f"{attr}: {value}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        game = cache.get(f"{self.room_group_name}_game_state")

        if game:
            print(f"Disconnecting ... Game state: {game}")
            game.stop_game()
            game.reset_game()
            print(f"After reset: Ball position: {game.ball.x}, {game.ball.y}")
            print(f"after stop: game.started: {game.started}")
            cache.set(f"{self.room_group_name}_game_state", game)

        # por enquanto está deletando quando o usuário desconecta, o que pode deixar o outro jogador sem saber que o outro saiu
        print("deleting from cache")
        cache.delete(f"{self.room_group_name}_game_state")

    async def receive(self, text_data):
        # processa mensagem recebida do cliente
        text_data_json = json.loads(text_data)
        # print(f"text_data_json: {text_data_json}")
        message_type = text_data_json["type"]

        if message_type == "join_room":
            await self.add_to_group(text_data_json["room_id"])
            game = await self.initialize_game_state(
                text_data_json["width"], text_data_json["height"]
            )
            await self.assign_player(game)
            await self.send_game_init(game)

            if not game.started:
                print("Starting worker")
                await self.start_worker(game)

    async def add_to_group(self, room_id):
        self.room_id = room_id
        self.room_group_name = f"pong_{self.room_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def initialize_game_state(self, width, height):
        # verifica se já existe um jogo em andamento se não cria um novo
        game = cache.get(f"{self.room_group_name}_game_state")
        if not game:
            game = PongGame(width, height)
            cache.set(f"{self.room_group_name}_game_state", game)
        return game

    async def assign_player(self, game):
        # adiciona o jogador ao jogo
        game.add_player(self.scope["user"].id, self.scope["user"].username)

    async def send_game_init(self, game):
        # envia o estado inicial do jogo para o cliente
        message = {"type": "game_init", "game_state": game.get_game_state()}
        print(f"message: {message}")
        await self.send(text_data=json.dumps(message))

    async def send_game_state(self, event):
        # envia o estado do jogo atualizado para o cliente
        game_state = event["game_state"]
        message = {"type": "update_game_state", "game_state": game_state}
        await self.send(text_data=json.dumps(message))

    async def start_worker(self, game):
        # inicia o jogo e envia uma tarefa para o worker processar o estado do jogo
        game.start_game()
        cache.set(f"{self.room_group_name}_game_state", game)

        # envia a tarefa para o worker
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "update_game_state",
                "room_group_name": self.room_group_name,
            },
        )
