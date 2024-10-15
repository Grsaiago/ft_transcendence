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


class PongRoom(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
