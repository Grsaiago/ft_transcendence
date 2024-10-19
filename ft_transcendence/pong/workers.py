import asyncio

from channels.consumer import AsyncConsumer
from django.core.cache import cache


class PongGameWorker(AsyncConsumer):
    async def update_game_state(self, message):
        room_group_name = message["room_group_name"]
        game = cache.get(f"{room_group_name}_game_state")

        if game and game.started:
            # atualiza o estado do jogo
            game.game_loop()
            cache.set(f"{room_group_name}_game_state", game)

            # envia o estado atualizado para o grupo de websockets
            await self.channel_layer.group_send(
                room_group_name,
                {
                    "type": "send_game_state",
                    "game_state": game.get_game_state(),
                },
            )

            # pequena pausa para simular a velocidade do jogo (60fps)
            await asyncio.sleep(0.016666)

            # reenvia a tarefa para si mesmo para continuar processando o estado do jogo
            await self.channel_layer.send(
                "pong_update_channel",
                {
                    "type": "update_game_state",
                    "room_group_name": room_group_name,
                },
            )
