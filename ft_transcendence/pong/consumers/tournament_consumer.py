import json
import logging

from asgiref.sync import sync_to_async
from django.core.cache import cache
from pong.models import Match, PongRoom, Tournament, TournamentParticipant
from user_management.models import TrUser

from .online_consumer import OnlinePongConsumer

logger = logging.getLogger(__name__)


class TournamentPongConsumer(OnlinePongConsumer):
    # Methods to interact with the database
    @sync_to_async
    def get_first_match_by_room(self, room):
        return Match.objects.filter(room=room).first()

    @sync_to_async
    def get_tournament_by_id(self, tournament_id):
        return TournamentParticipant.objects.get(id=tournament_id)

    @sync_to_async
    def get_match_with_related(self, match_id: int) -> Match:
        return Match.objects.select_related(
            "room__tournament", "player1", "player2"
        ).get(id=match_id)

    @sync_to_async
    def eliminate_player(self, tournament: Tournament, user: TrUser) -> None:
        return tournament.participants.filter(player=user).update(is_eliminated=True)

    @sync_to_async
    def get_alive_count(self, tournament: Tournament) -> int:
        return tournament.participants.filter(is_eliminated=False).count()

    @sync_to_async
    def finalize_tournament(self, tournament: Tournament) -> None:
        tournament.is_active = False
        tournament.save()

    @sync_to_async
    def get_winner(self, match):
        """
        Retrieves the winner of the match.
        """
        return match.winner

    async def start_game(self) -> bool:
        """
        Starts the game when both players are ready.
        In tournament mode, the game only starts when both players are ready, and the match ID is fetched from the database.
        """
        try:
            if not self.is_ready:
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
                        room = await self.get_room_by_id(self.room_id)
                        match = await self.get_first_match_by_room(room)

                        if not match:
                            raise Exception("No match found for the given room.")

                        self.match_id = match.id
                        cache.set(f"{self.room_group_name}_match_id", self.match_id)
                        logger.info(f"Match ID set to {self.match_id}")
                        await self.worker_start_game()
                        return True
        except Exception as e:
            await self.send_error("Failed to start game.")
            logger.exception(f"Failed to start game: {e}")
        return False

    async def define_winner(self, event) -> None:
        """
        Defines the winner of the tournament match and redirects the player to the tournament hub.
        """
        try:
            await super().define_winner(event)
            room = await self.get_room_by_id(self.room_id)
            match = await self.get_first_match_by_room(room)
            await self.advance_tournament(match.id)
            await self.redirect_to_hub()
        except Exception as e:
            await self.send_error("Failed to define winner in tournament.")
            logger.exception(f"Failed to define winner in tournament: {e}")

    async def redirect_to_hub(self) -> None:
        """
        Redirects the player back to the tournament hub after the match concludes.
        """
        try:
            room = await self.get_room_by_id(self.room_id)
            tournament_id = room.tournament.id
            if tournament_id:
                tournament_url = f"/tournament/{tournament_id}"
                await self.send_redirect(tournament_url)
            logger.info(f"Redirecting player to tournament hub at {tournament_url}")
        except PongRoom.DoesNotExist:
            await self.send_error("Room not found for redirection.")
            logger.error("Room not found when attempting to redirect to hub.")
        except AttributeError:
            await self.send_error("Tournament ID not found for redirection.")
            logger.error(
                "Tournament ID not found in room when attempting to redirect to hub."
            )

    async def finish_game(self) -> None:
        """
        Cleans up after the game finishes in tournament mode and redirects the player to the hub.
        """
        await super().finish_game()

    async def get_bracket_mapping(self, tournament: Tournament):

        # Retorna um dicionário indicando para onde vai o vencedor de cada partida.
        # Formato: {match_id: (next_match_id, player_slot)}
        # player_slot = 1 ou 2, indicando se o vencedor vai em player1 ou player2 da próxima match.

        matches = await sync_to_async(list)(
            Match.objects.filter(room__tournament=tournament).order_by("id")
        )

        if tournament.max_players == 4:
            # Supondo que as partidas são criadas na ordem: Semi1, Semi2, Final
            # Recupera os IDs após criação do bracket
            semi1, semi2, final = matches[:3]
            return {
                semi1.id: (final.id, 1),  # Vencedor Semi1 -> Final.player1
                semi2.id: (final.id, 2),  # Vencedor Semi2 -> Final.player2
            }
        elif tournament.max_players == 8:
            # Supondo que as partidas são criadas na ordem: QF1-4, Semi1-2, Final
            quarter_finals = matches[:4]
            semi_finals = matches("id")[4:6]
            final = matches("id")[6]
            return {
                quarter_finals[0].id: (
                    semi_finals[0].id,
                    1,
                ),  # Vencedor QF1 -> Semi1.player1
                quarter_finals[1].id: (
                    semi_finals[0].id,
                    2,
                ),  # Vencedor QF2 -> Semi1.player2
                quarter_finals[2].id: (
                    semi_finals[1].id,
                    1,
                ),  # Vencedor QF3 -> Semi2.player1
                quarter_finals[3].id: (
                    semi_finals[1].id,
                    2,
                ),  # Vencedor QF4 -> Semi2.player2
                semi_finals[0].id: (final.id, 1),  # Vencedor Semi1 -> Final.player1
                semi_finals[1].id: (final.id, 2),  # Vencedor Semi2 -> Final.player2
            }

    async def advance_tournament(self, match_id: int):
        match = await self.get_match_with_related(match_id)
        tournament = match.room.tournament

        winner = await self.get_winner(match)

        loser = match.player1 if match.player1 != winner else match.player2
        await self.eliminate_player(tournament, loser)

        alive_count = await self.get_alive_count(tournament)
        if alive_count == 1:
            tournament.winner = winner
            await self.finalize_tournament(tournament)
        else:
            bracket_mapping = await self.get_bracket_mapping(tournament)

            if match.id in bracket_mapping:
                next_match_index, player_slot = bracket_mapping[match.id]
                next_match = await self.get_match_with_related(next_match_index)
                if player_slot == 1:
                    next_match.player1 = winner
                else:
                    next_match.player2 = winner

                await sync_to_async(next_match.save)()
                logger.info(
                    f"Assigned winner {match.winner.username} to match {next_match.id} as player {player_slot}"
                )

    # Methods to send messages to the client
    async def send_redirect(self, url: str) -> None:
        """
        Sends a redirect message to the client.
        """
        await self.send(
            text_data=json.dumps({"type": "redirect_tournament", "redirect": url})
        )
