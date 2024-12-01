import asyncio
from typing import List, Optional

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.core.cache import cache
from pong.models import Match, PongRoom
from user_management.models import TrUser

from .base_consumer import (
    BasePongConsumer,
    ClientMessage,
    Direction,
    GameStateEvent,
    Paddle,
    logger,
)


class OnlinePongConsumer(BasePongConsumer):
    """
    OnlinePongConsumer handles the game logic for online (multiplayer) games.
    Inherits from BasePongConsumer.
    """

    async def connect(self) -> None:
        """
        Handles the WebSocket connection event.
        Initializes online game-specific variables.
        """
        await super().connect()
        self.player_paddle: Optional[str] = None
        self.is_spectator: bool = False
        self.is_ready: bool = False

        # Initialize variables that will be used after join_room
        self.ready_players: int = 0
        self.players_data: List[int] = []
        self.match_id: Optional[int] = None

        self.ready_lock = asyncio.Lock()

    async def handle_join_room(self, data: ClientMessage) -> None:
        """
        Handles the 'join_room' message from the client.

        Args:
            data (ClientMessage): The data received from the client.
        """
        try:
            self.room_id = data["room_id"]
            await self.add_to_group(self.room_id)

            # Now that self.room_group_name is initialized
            async with self.ready_lock:
                self.players_data = cache.get(f"{self.room_group_name}_players", [])
                self.ready_players = cache.get(
                    f"{self.room_group_name}_ready_players", 0
                )
                self.match_id = cache.get(f"{self.room_group_name}_match_id", None)

                if (
                    len(self.players_data) < 2
                    and self.scope["user"].id not in self.players_data
                ):
                    self.player_paddle = (
                        Paddle.LEFT if not self.players_data else Paddle.RIGHT
                    )
                    self.players_data.append(self.scope["user"].id)
                    cache.set(f"{self.room_group_name}_players", self.players_data)
                elif self.scope["user"].id in self.players_data:
                    # Reassign the paddle if the user reconnects
                    index = self.players_data.index(self.scope["user"].id)
                    self.player_paddle = Paddle.LEFT if index == 0 else Paddle.RIGHT
                    self.is_spectator = self.ready_players > index
                else:
                    self.is_spectator = True

            await self.initialize_game_data(data["width"], data["height"])
            await self.worker_initialize_game()
        except Exception as e:
            await self.send_error("Failed to join room.")
            logger.exception(f"Failed to handle join_room: {e}")

    async def start_game(self) -> bool:
        """
        Starts the game when both players are ready.
        In online game mode, the game only starts when both players are ready, that is, they press play
        """
        try:
            if not self.is_spectator and not self.is_ready:
                async with self.ready_lock:
                    self.ready_players = cache.get(
                        f"{self.room_group_name}_ready_players", 0
                    )
                    self.ready_players += 1
                    self.is_ready = True
                    cache.set(
                        f"{self.room_group_name}_ready_players", self.ready_players
                    )
                    logger.info(
                        f"Player {self.scope['user'].id} is ready. Total ready players: {self.ready_players}"
                    )

                    if self.ready_players == 2:
                        self.match_id = cache.get(
                            f"{self.room_group_name}_match_id", None
                        )
                        if not self.match_id:
                            await self.worker_start_game()
                            await self.create_match()
                            return True
        except Exception as e:
            await self.send_error("Failed to start game.")
            logger.exception(f"Failed to start game: {e}")
        return False

    async def handle_key_paddle_event(self, key: str, state: bool) -> None:
        """
        Handles key events from the client for moving paddles.

        Args:
            key (str): The key that was pressed or released.
            state (bool): True if the key is pressed, False if it is released.
        """
        try:
            if self.is_spectator:
                return

            paddle = self.player_paddle
            if key in ["w", "arrowup"]:
                direction = Direction.UP
            elif key in ["s", "arrowdown"]:
                direction = Direction.DOWN
            else:
                logger.warning(f"Unhandled key: {key}")
                return

            await self.worker_update_paddles_position(paddle, direction, state)
        except Exception as e:
            await self.send_error("Failed to handle key event.")
            logger.exception(f"Failed to handle key_paddle_event: {e}")

    async def finish_game(self) -> None:
        """
        Performs any necessary cleanup when the game ends.
        """
        try:
            if self.scope["user"].id in self.players_data:
                self.players_data.remove(self.scope["user"].id)
                cache.set(f"{self.room_group_name}_players", self.players_data)

            if len(self.players_data) == 0:
                # Send a message to the worker to finish the game
                await self.channel_layer.send(
                    "pong_update_channel",
                    {
                        "type": "finish_game",
                        "room_id": str(self.room_id),
                    },
                )
                # Clear the cache of game-related variables
                cache.delete(f"{self.room_group_name}_players")
                cache.delete(f"{self.room_group_name}_game_data")
                cache.delete(f"{self.room_group_name}_ready_players")
                cache.delete(f"{self.room_group_name}_match_id")
                logger.info(
                    f"Game finished and cleaned up for room {self.room_group_name}"
                )

            if self.room_group_name:
                # Remove the user from the group
                await self.channel_layer.group_discard(
                    self.room_group_name, self.channel_name
                )
        except Exception as e:
            await self.send_error("Failed to finish game.")
            logger.exception(f"Failed to finish game: {e}")

    async def define_winner(self, event: GameStateEvent) -> None:
        """
        Defines the winner based on the game state received from the worker.

        Args:
            event (GameStateEvent): The event data containing the game state.
        """
        try:
            if self.is_spectator:
                return

            async with self.ready_lock:
                match_id = cache.get(f"{self.room_group_name}_match_id", None)
                if match_id:
                    match = await self.get_match_by_id(match_id)
                    if match.winner is None:
                        winner_side = event["game_state"]["winner"]
                        if winner_side == Paddle.LEFT:
                            match.winner = match.player1
                        else:
                            match.winner = match.player2
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
        except Exception as e:
            await self.send_error("Failed to define winner.")
            logger.exception(f"Failed to define winner: {e}")

    # Online mode helper methods
    async def create_match(self) -> None:
        """
        Creates a new match record in the database.
        """
        try:
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
                logger.info(f"Match created: {match}")
        except Exception as e:
            await self.send_error("Failed to create match.")
            logger.exception(f"Failed to create match: {e}")

    async def get_player_by_id(self, player_id: int) -> TrUser:
        """
        Retrieves a player (User) by ID.

        Args:
            player_id (int): The ID of the player.

        Returns:
            User (TrUser): The User object corresponding to the player ID.
        """
        return await sync_to_async(get_user_model().objects.get)(id=player_id)

    async def get_pongroom_by_id(self, room_id: int) -> PongRoom:
        """
        Retrieves a PongRoom by ID.

        Args:
            room_id (int): The ID of the PongRoom.

        Returns:
            PongRoom: The PongRoom object corresponding to the room ID.
        """
        return await sync_to_async(PongRoom.objects.get)(id=room_id)

    async def get_match_by_id(self, match_id: int) -> Match:
        """
        Retrieves a Match by ID, selecting related player1 and player2.

        Args:
            match_id (int): The ID of the Match.

        Returns:
            Match: The Match object corresponding to the match ID.
        """
        return await sync_to_async(
            lambda: Match.objects.select_related("player1", "player2").get(id=match_id)
        )()
