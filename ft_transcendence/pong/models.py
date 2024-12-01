from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models

# Cada sala é um jogo?
#   Não. Cada sala é um espaço onde pode ter um jogo.
# - Eu posso criar uma sala e esperar alguém entrar ou eu posso entrar em uma sala que já existe.
# - Eu posso convidar alguém para entrar na minha sala.
# - Eu posso aceitar ou recusar um convite para entrar em uma sala.
# - Eu posso sair de uma sala.
# - Eu posso excluir uma sala.
# - Eu posso ver quem está na sala.
# - Eu posso ver o histórico de jogos da sala.
# - Eu posso ver o placar da sala. Não sei? faz sentido? Será que cada sala deveria ser um jogo?


class GameMode(Enum):
    LOCAL = "local"
    ONLINE = "online"
    TOURNAMENT = "tournament"

    @classmethod
    def choices(cls):
        return [(gameMode.value, gameMode.name.capitalize()) for gameMode in cls]

    @classmethod
    def as_dict(cls):
        return {gameMode.name: gameMode.value for gameMode in cls}


class PongRoom(models.Model):
    # limitando o nome da sala para 50 caracteres pois channel_name é limitado a 100 caracteres
    name = models.CharField(max_length=50)
    game_mode = models.CharField(max_length=20, choices=GameMode.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"PongRoom id: {self.id}. Room name: {self.name} - Game_mode: {self.game_mode}"


class Match(models.Model):
    room = models.ForeignKey(PongRoom, on_delete=models.CASCADE, related_name="matches")
    player1 = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="player1"
    )
    player2 = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="player2"
    )
    winner = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match id: {self.id}. Room id: {self.room_id} - Player1_id: {self.player1_id} vs Player2_id: {self.player2_id}"


class UserMatchStats(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    total_matches = models.PositiveIntegerField(default=0)
    total_wins = models.PositiveIntegerField(default=0)

    def increment_matches(self):
        self.total_matches += 1
        self.save()

    def increment_wins(self):
        self.total_wins += 1
        self.save()

    def __str__(self):
        return f"{self.id}:{self.user.username} - Matches: {self.total_matches}, Wins: {self.total_wins}"
