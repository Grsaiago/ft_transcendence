from django import forms

from .models import PongRoom, Tournament


class PongRoomForm(forms.ModelForm):
    class Meta:
        model = PongRoom
        fields = ["name"]
        labels = {
            "name": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "pong-room-form-input",
                    "placeholder": "Crie um nome de sala",
                    "title": "Escolha um nome para a sala. Tamanho máximo: 50 caracteres.",
                }
            ),
        }


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name"]
        labels = {
            "name": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "pong-room-form-input",
                    "placeholder": "Crie um nome de torneio",
                    "title": "Escolha um nome para o torneio. Tamanho máximo: 50 caracteres.",
                }
            ),
        }
