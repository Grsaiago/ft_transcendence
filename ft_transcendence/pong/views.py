from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import PongRoomForm
from .models import PongRoom


class PongEnterView(TemplateView):
    template_name = "pong/enter.html"

    def get(self, request, *args, **kwargs):
        form = PongRoomForm()
        rooms = PongRoom.objects.all()
        return self.render_to_response({"form": form, "rooms": rooms})

    def post(self, request, *args, **kwargs):
        form = PongRoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            return redirect("pong:pongroom", room_id=room.id)
        rooms = PongRoom.objects.all()
        return self.render_to_response({"form": form, "rooms": rooms})


class PongRoomView(TemplateView):
    template_name = "pong/room.html"

    def get(self, request, *args, **kwargs):
        room = PongRoom.objects.get(id=kwargs["room_id"])
        return self.render_to_response({"room": room})
