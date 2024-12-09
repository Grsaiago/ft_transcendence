import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# from django.contrib.auth import get_user_model
from pong.models import Match, PongRoom, Tournament, TournamentParticipant
from user_management.models import TrUser

logger = logging.getLogger(__name__)


class TournamentConsumerHub(AsyncWebsocketConsumer):
    async def connect(self):
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournament_id"]
        self.tournament_group_name = f"tournament_{self.tournament_id}"
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.accept()
            await self.send(
                text_data=json.dumps(
                    {{"type": "not_auth", "message": "User not authenticated"}}
                )
            )
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.tournament_group_name, self.channel_name
            )
            await self.accept()
            await self.send_current_tournament_state()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.tournament_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data["type"]

        if message_type == "join_tournament":
            joined = await self.join_tournament()
            if joined:
                await self.check_start_tournament()

    async def join_tournament_db(self) -> bool:
        try:
            tournament = await sync_to_async(Tournament.objects.get)(
                id=self.tournament_id
            )
            if tournament:
                count = tournament.participants.count()
                if count < tournament.max_players:
                    already_joined = await sync_to_async(
                        TournamentParticipant.objects.filter
                    )(tournament=tournament, user=self.user)
                    if not already_joined:
                        TournamentParticipant.objects.create(
                            tournament=tournament, user=self.user
                        )
                        logger.info(
                            f"User {self.user.username} joined tournament {tournament.name}"
                        )
                        return True
        except Exception as e:
            await self.send_error(f"Error joining tournament {self.tournament_id}")
            logger.exception(f"Error joining tournament {self.tournament_id}: {e}")
        return False

    async def join_tournament(self) -> bool:
        joined = await self.join_tournament_db()
        if joined:
            await self.channel_layer.group_send(
                self.tournament_group_name,
                {
                    "type": "tounament_update",
                    "message": f"{self.user.username} joined the tournament",
                },
            )
            return True
        return False

    async def check_start_tournament(self):
        tournament = await sync_to_async(Tournament.objects.get)(id=self.tournament_id)
        if tournament.participants.count() == tournament.max_players:
            await self.start_tournament(tournament)

    async def start_tournament(self, tournament: Tournament):
        await self.create_initial_matches(tournament)
        # send message to all participants informing the tournament has started
        await self.channel_layer.group_send(
            self.tournament_group_name,
            {"type": "tournament_update", "message": "Tournament has started!"},
        )

    async def create_initial_matches(self, tournament: Tournament):
        try:
            participants = await sync_to_async(TournamentParticipant.objects.filter)(
                tournament=tournament
            )
            participants = list(participants)
            for i in range(0, len(participants), 2):
                player1 = participants[i]
                player2 = participants[i + 1]
                room = PongRoom.objects.create(
                    name=f"{tournament.name} - Match {i // 2}",
                    game_mode="tournament",
                    tournament=tournament,
                )
                Match.objects.create(room=room, player1=player1, player2=player2)
        except Exception as e:
            await self.send_error("Failed to create initial matches")
            logger.exception(f"Failed to create initial matches: {e}")

    async def create_match(
        self, player1: TrUser, player2: TrUser, room: PongRoom
    ) -> None:
        """
        Creates a new match record in the database.

        Args:
            player1 (TrUser): The first player in the match.
            player2 (TrUser): The second player in the match.
            room (PongRoom): The room in which the match will be played.
        """
        try:
            match = await sync_to_async(Match.objects.create)(
                room=room,
                player1=player1,
                player2=player2,
            )
            logger.info(f"Tournament match created: {match}")
        except Exception as e:
            await self.send_error("Failed to create match.")
            logger.exception(f"Failed to create match: {e}")

    async def tournament_update(self, event):
        message = event["message"]
        tournament = await sync_to_async(Tournament.objects.get)(id=self.tournament_id)
        matches = await sync_to_async(
            lambda: list(Match.objects.filter(room__tournament=tournament))
        )()

        matches_info = []
        for match in matches:
            matches_info.append(
                {
                    "id": match.id,
                    "player1": match.player1.id,
                    "player2": match.player2.id,
                    "room_id": match.room.id,
                }
            )

        await self.send(
            text_data=json.dumps(
                {
                    "event": "tournament_update",
                    "message": message,
                    "matches": matches_info,
                }
            )
        )

    async def send_current_state(self):
        tournament = await sync_to_async(Tournament.objects.get)(id=self.tournament_id)
        participants = await sync_to_async(
            lambda: list(tournament.participants.select_related("player").all())
        )()
        participant_list = [p.player.username for p in participants]

        await self.send(
            text_data=json.dumps(
                {
                    "event": "current_state",
                    "participants": participant_list,
                    "max_players": tournament.max_players,
                    "is_active": tournament.is_active,
                }
            )
        )

    async def tournament_advance(self, event):
        next_match_info = event["next_match_info"]
        await self.send(
            text_data=json.dumps(
                {"event": "tournament_advance", "next_match": next_match_info}
            )
        )

    # Utility methods
    async def send_error(self, message: str) -> None:
        """
        Sends an error message to the client.

        Args:
            message (str): The error message to send.
        """
        await self.send(text_data=json.dumps({"type": "error", "message": message}))
