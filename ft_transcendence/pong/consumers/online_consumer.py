import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.core.cache import cache
from pong.models import Match

from .base_consumer import BasePongConsumer


class OnlinePongConsumer(BasePongConsumer):
    async def connect(self):
        await super().connect()
        self.player_paddle = None
        self.is_spectator = False
        self.is_ready = False

        self.ready_players = cache.get(f"{self.room_group_name}_ready_players", 0)
        self.players_data = cache.get(f"{self.room_group_name}_players", [])

        self.ready_lock = asyncio.Lock()

    async def join_room(self, data):
        self.room_id = data["room_id"]
        await self.add_to_group(self.room_id)

        async with self.ready_lock:
            self.players_data = cache.get(f"{self.room_group_name}_players", [])

            if (
                len(self.players_data) < 2
                and self.scope["user"].username not in self.players_data
            ):
                self.player_paddle = "left" if not self.players_data else "right"
                self.players_data.append(self.scope["user"].username)
                cache.set(f"{self.room_group_name}_players", self.players_data)
            elif self.scope["user"].username in self.players_data:
                # reatribuir o paddle caso o usuário se reconecte
                self.player_paddle = (
                    "left"
                    if self.players_data.index(self.scope["user"].username) == 0
                    else "right"
                )
                self.is_spectator = self.ready_players > self.players_data.index(
                    self.scope["user"].username
                )
            else:
                self.is_spectator = True

        await self.initialize_game_data(data["width"], data["height"])
        await self.worker_initialize_game()

    async def start_game(self):
        # começar o jogo apenas quanto ambos estiverem prontos
        if not self.is_spectator and not self.is_ready:
            async with self.ready_lock:
                self.ready_players = cache.get(
                    f"{self.room_group_name}_ready_players", 0
                )
                self.ready_players += 1
                self.is_ready = True
                cache.set(f"{self.room_group_name}_ready_players", self.ready_players)

                if self.ready_players == 2:
                    players_data = cache.get(f"{self.room_group_name}_players", [])
                    if players_data:
                        player1 = await self.get_user_by_username(players_data[0])
                        player2 = await self.get_user_by_username(players_data[1])

                        match = sync_to_async(Match.objects.create)(
                            room_id=self.room_id,
                            player1=player1,
                            player2=player2,
                        )
                        print(match)

                    await self.worker_start_game()

    async def handle_key_paddle_event(self, key, state):
        if self.is_spectator:
            return

        paddle = self.player_paddle
        if key in ["w", "arrowup"]:
            direction = "up"
        elif key in ["s", "arrowdown"]:
            direction = "down"
        else:
            return

        await self.worker_update_paddles_position(paddle, direction, state)

    async def finish_game(self):
        if self.scope["user"].username in self.players_data:
            self.players_data.remove(self.scope["user"].username)
            cache.set(f"{self.room_group_name}_players", self.players_data)

        if len(self.players_data) == 0:
            # envia mensagem para o worker para finalizar o jogo
            await self.channel_layer.send(
                "pong_update_channel",
                {
                    "type": "finish_game",
                    "room_id": str(self.room_id),
                },
            )
            # Limpa o cache das variáveis relacionadas ao jogo
            cache.delete(f"{self.room_group_name}_players")
            cache.delete(f"{self.room_group_name}_game_data")
            cache.delete(f"{self.room_group_name}_ready_players")

        if self.room_group_name:
            # remove o usuário do grupo
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    # métodos auxiliares para OnlinePongConsumer
    async def get_user_by_username(self, username):
        User = get_user_model()
        return await sync_to_async(User.objects.get)(username=username)
