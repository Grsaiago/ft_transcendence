from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView

from .forms import PongRoomForm
from .models import GameMode, PongRoom


class PongSelectGameMode(TemplateView):
    template_name = "pong/play.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"GameMode": GameMode.as_dict()})

    def post(self, request, *args, **kwargs):
        game_mode = request.POST.get("game_mode")
        print(game_mode)
        if game_mode == GameMode.LOCAL.value:
            room_name = f"Local-{get_random_string(8)}"
            room = PongRoom.objects.create(
                name=room_name, game_mode=GameMode.LOCAL.value
            )
            return redirect("pong:pongroom", room_id=room.id)
        else:
            return redirect("pong:pongenter", game_mode=game_mode)


class PongEnterView(TemplateView):
    template_name = "pong/enter.html"

    def get(self, request, *args, **kwargs):
        form = PongRoomForm()
        game_mode = kwargs["game_mode"]
        rooms = PongRoom.objects.filter(game_mode=game_mode)
        return self.render_to_response(
            {"form": form, "rooms": rooms, "game_mode": game_mode}
        )

    def post(self, request, *args, **kwargs):
        game_mode = kwargs["game_mode"]
        form = PongRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.game_mode = game_mode
            room = form.save()
            return redirect("pong:pongroom", room_id=room.id)
        rooms = PongRoom.objects.filter(game_mode=game_mode)
        return self.render_to_response({"form": form, "rooms": rooms})


class PongRoomView(TemplateView):
    template_name = "pong/room.html"

    def get(self, request, *args, **kwargs):
        room = PongRoom.objects.get(id=kwargs["room_id"])
        print(room)
        return self.render_to_response({"room": room, "game_mode": room.game_mode})
