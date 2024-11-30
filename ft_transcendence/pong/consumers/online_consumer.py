import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.core.cache import cache
from pong.models import Match, PongRoom

from .base_consumer import BasePongConsumer

# import json


class OnlinePongConsumer(BasePongConsumer):
    async def connect(self):
        await super().connect()
        self.player_paddle = None
        self.is_spectator = False
        self.is_ready = False

        self.ready_players = cache.get(f"{self.room_group_name}_ready_players", 0)
        self.players_data = cache.get(f"{self.room_group_name}_players", [])
        self.match_id = cache.get(f"{self.room_group_name}_match_id", None)

        self.ready_lock = asyncio.Lock()

    async def join_room(self, data):
        self.room_id = data["room_id"]
        await self.add_to_group(self.room_id)

        async with self.ready_lock:
            self.players_data = cache.get(f"{self.room_group_name}_players", [])

            if (
                len(self.players_data) < 2
                and self.scope["user"].id not in self.players_data
            ):
                self.player_paddle = "left" if not self.players_data else "right"
                self.players_data.append(self.scope["user"].id)
                cache.set(f"{self.room_group_name}_players", self.players_data)
            elif self.scope["user"].id in self.players_data:
                # reatribuir o paddle caso o usuário se reconecte
                self.player_paddle = (
                    "left"
                    if self.players_data.index(self.scope["user"].id) == 0
                    else "right"
                )
                self.is_spectator = self.ready_players > self.players_data.index(
                    self.scope["user"].id
                )
            else:
                self.is_spectator = True

        await self.initialize_game_data(data["width"], data["height"])
        await self.worker_initialize_game()

    async def start_game(self):
        # começar o jogo apenas quando ambos estiverem prontos
        if not self.is_spectator and not self.is_ready:
            async with self.ready_lock:
                self.ready_players = cache.get(
                    f"{self.room_group_name}_ready_players", 0
                )
                self.ready_players += 1
                self.is_ready = True
                cache.set(f"{self.room_group_name}_ready_players", self.ready_players)

                if self.ready_players == 2:
                    self.match_id = cache.get(f"{self.room_group_name}_match_id", None)
                    if not self.match_id:
                        await self.worker_start_game()
                        await super().start_game()
                        await self.create_match()

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
        if self.scope["user"].id in self.players_data:
            self.players_data.remove(self.scope["user"].id)
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

    async def define_winner(self, event):
        if self.is_spectator:
            return

        async with self.ready_lock:
            match_id = cache.get(f"{self.room_group_name}_match_id", None)
            if match_id:
                match = await self.get_match_by_id(match_id)
                if match.winner is None:
                    winner_side = event["game_state"]["winner"]
                    if winner_side == "left":
                        match.winner = await self.get_player_by_id(match.player1.id)
                    else:
                        match.winner = await self.get_player_by_id(match.player2.id)
                    self.winner = match.winner.username
                    match.finished = True
                    await sync_to_async(match.save)()
                    self.ready_players = 0
                    self.is_ready = False
                    self.match_id = None
                    cache.set(
                        f"{self.room_group_name}_ready_players",
                        self.ready_players,
                    )
                    cache.set(f"{self.room_group_name}_match_id", self.match_id)
                else:
                    self.winner = None

    # métodos de online_consumer
    async def create_match(self):
        players_data = cache.get(f"{self.room_group_name}_players", [])
        if players_data:
            player1 = await self.get_player_by_id(players_data[0])
            player2 = await self.get_player_by_id(players_data[1])
            pongroom = await self.get_pongroom_by_id(self.room_id)

            match = await sync_to_async(Match.objects.create)(
                room=pongroom,
                player1=player1,
                player2=player2,
            )
            cache.set(f"{self.room_group_name}_match_id", match.id)
            print(match)

    async def get_player_by_id(self, player_id):
        return await sync_to_async(get_user_model().objects.get)(id=player_id)

    async def get_pongroom_by_id(self, room_id):
        return await sync_to_async(PongRoom.objects.get)(id=room_id)

    async def get_match_by_id(self, match_id):
        return await sync_to_async(
            lambda: Match.objects.select_related("player1", "player2").get(id=match_id)
        )()
