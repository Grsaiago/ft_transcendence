import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class BasePongConsumer(AsyncWebsocketConsumer):
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
            # remove os dados do jogo
            cache.delete(f"{self.room_group_name}_game_data")

    async def receive(self, text_data):
        # processa mensagem recebida do cliente
        text_data_json = json.loads(text_data)
        type = text_data_json["type"]

        if type == "join_room":
            print("join_room")
            self.room_id = text_data_json["room_id"]
            await self.add_to_group(self.room_id)
            await self.initialize_game_data(
                text_data_json["width"], text_data_json["height"]
            )
            await self.worker_initialize_game()

        elif type == "start_game":
            print("start_game")
            await self.worker_start_game()

        elif type in ["keydown", "keyup"]:
            key = text_data_json["key"]
            state = type == "keydown"  # True se for keydown, False se for keyup
            await self.handle_key_paddle_event(key, state)

    async def add_to_group(self, room_id):
        print("add_to_group")
        self.room_group_name = f"pong_{self.room_id}"
        self.game_data = cache.get(f"{self.room_group_name}_game_data", {})
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def initialize_game_data(self, width, height):
        print("initialize_game_data")
        # verifica se já existe dados do jogo em andamento se não cria um novo
        if not self.game_data:
            self.game_data["width"] = width
            self.game_data["height"] = height
            cache.set(f"{self.room_group_name}_game_data", self.game_data)

        # adicionar dados necessários para o jogo, como os jogadores?

    async def worker_initialize_game(self):
        print("worker_initialize_game")
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

    async def worker_update_paddles_position(self, paddle, direction, state):
        # envia mensagem para o worker e atualiza as variáveis dos paddles
        await self.channel_layer.send(
            "pong_update_channel",
            {
                "type": "update_paddles_position",
                "room_id": str(self.room_id),
                "paddle": paddle,  # left ou right
                "direction": direction,  # up ou down
                "state": state,  # True se for keydown, False se for keyup
            },
        )

    async def handle_key_paddle_event(self, key, state):
        pass  # implementar nas classes filhas

    async def send_game_state(self, event):
        # Recebe o estado do worker
        game_state = event["game_state"]

        # Envia o estado do jogo para o cliente WebSocket
        await self.send(
            text_data=json.dumps({"type": "game_init", "game_state": game_state})
        )

    async def get_winner(self, event):
        # Recebe o estado do worker
        game_state = event["game_state"]

        winner = game_state["winner"]
        if winner:
            print("winner", winner)
            # envia uma mensagem para o cliente informando o vencedor
            await self.send(text_data=json.dumps({"type": "winner", "winner": winner}))
