from django.core.cache import cache

from .base_consumer import BasePongConsumer


class LocalPongConsumer(BasePongConsumer):
    async def join_room(self, data):
        self.room_id = data["room_id"]
        await self.add_to_group(self.room_id)
        await self.initialize_game_data(data["width"], data["height"])
        await self.worker_initialize_game()

    async def start_game(self):
        await super().start_game()
        # no modo local inicia imediatemento ao precionar Start e receber a msg star_game
        await self.worker_start_game()

    async def handle_key_paddle_event(self, key, state):
        # mapeia as para os paddle no modo local
        # w e s para o paddle esquerdo
        # arrowup e arrowdown para o paddle direito
        if key in ["w", "s"]:
            paddle = "left"
            direction = "up" if key == "w" else "down"
        elif key in ["arrowup", "arrowdown"]:
            paddle = "right"
            direction = "up" if key == "arrowup" else "down"

        await self.worker_update_paddles_position(paddle, direction, state)

    async def finish_game(self):
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
