import logging

from asgiref.sync import sync_to_async
from django.core.cache import cache
from pong.models import Match, PongRoom, TournamentParticipant

from .online_consumer import OnlinePongConsumer

logger = logging.getLogger(__name__)


class TournamentPongConsumer(OnlinePongConsumer):
    async def start_game(self) -> bool:
        """
        Starts the game when both players are ready.
        In tournament mode, the game only starts when both players are ready, and the match ID is fetched from the database.
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
                        # Buscar match_id no banco de dados com base no ID da sala
                        room = await sync_to_async(PongRoom.objects.get)(
                            id=self.room_id
                        )
                        # Buscar o primeiro match associado à sala
                        match = await sync_to_async(
                            lambda: Match.objects.filter(room=room).first()
                        )()
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

    async def define_winner(self, event):
        await super().define_winner(event)
        # after define de winner, advance the tournament
        await self.notify_tournament_hub()

    async def notify_tournament_hub(self):
        match = await sync_to_async(Match.objects.get)(id=self.match_id)
        if match:
            next_match_info = await self.advance_tournament(match)
            if match.room and match.room.tournament:
                tournament_id = match.room.tournament.id
                await self.channel_layer.group_send(
                    f"tournament_{tournament_id}",
                    {
                        "type": "tournament_advance",
                        "next_match_info": next_match_info,
                    },
                )

    async def get_current_match(self):
        try:
            logger.info(f"Getting match with id {self.match_id}")
            return await sync_to_async(Match.objects.get)(id=self.match_id)
        except Exception as e:
            await self.send_error(f"Error getting match with id {self.match_id}")
            logger.exception(f"Error getting match with id {self.match_id}: {e}")
            return None

    async def advance_tournament(self, match):
        # Aqui implementamos a lógica de chaveamento básica.
        # Ajuste conforme sua necessidade. Abaixo um placeholder:
        return await sync_to_async(self.advance_tournament_logic)(match)

    def advance_tournament_logic(self, match):
        # Lógica simplificada:
        # - Se sobrar um único participante, torneio acaba.
        # - Caso contrário, criar próxima partida se necessário.

        tournament = match.room.tournament
        # Marca o perdedor como eliminado
        loser = match.player1 if match.winner != match.player1 else match.player2
        TournamentParticipant.objects.filter(
            tournament=tournament, player=loser
        ).update(is_eliminated=True)

        # Quantos ainda estão vivos?
        alive = tournament.participants.filter(is_eliminated=False)
        if alive.count() == 1:
            # Torneio finalizado
            tournament.is_active = False
            tournament.save()
            # Sem próxima partida
            return None
        else:
            # Exemplificando: se ainda tem mais de um jogador vivo,
            # criar uma próxima partida para o vencedor (match.winner) contra outro jogador disponível.
            # Encontrar outro jogador para emparelhar
            alive_players = [p.player for p in alive if p.player != match.winner]
            if not alive_players:
                # Nenhum outro jogador, então termina
                return None

            # Pegue o primeiro jogador vivo (exemplo simples)
            opponent = alive_players[0]
            # Cria nova sala e match
            next_room = PongRoom.objects.create(
                name=f"{tournament.name}-next-phase",
                game_mode="tournament",
                tournament=tournament,
            )
            next_match = Match.objects.create(
                room=next_room, player1=match.winner, player2=opponent
            )
            return {"room_id": next_match.room_id}
