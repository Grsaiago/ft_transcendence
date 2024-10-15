from django import forms

from .models import PongRoom


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
