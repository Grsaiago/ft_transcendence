from http.client import HTTPResponse
from django.http import JsonResponse
import logging

from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.views.generic import DetailView, TemplateView

from .forms import PongRoomForm, TournamentForm
from .models import GameMode, Match, PongRoom, Tournament, TournamentParticipant

logger = logging.getLogger(__name__)


class PongSelectGameMode(TemplateView):
    template_name = "../../user_management/templates/user_management/base_app.html"

    def get(self, request, *args, **kwargs):
        context = {"GameMode": GameMode.as_dict()}
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/play.html", context)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        game_mode = request.POST.get("game_mode")
        logger.info(f"Selected game_mode: {game_mode}")
        if game_mode == GameMode.LOCAL.value:
            room_name = f"Local-{get_random_string(8)}"
            room = PongRoom.objects.create(
                name=room_name, game_mode=GameMode.LOCAL.value
            )
            return redirect("pong:pongroom", room_id=room.id)
        else:
            logger.info(f"Redirecting to PongEnterView with game_mode: {game_mode}")
            return redirect("pong:pongenter", game_mode=game_mode)


class PongEnterView(TemplateView):
    template_name = "../../user_management/templates/user_management/base_app.html"
    # template_name = "pong/enter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_mode = kwargs.get("game_mode")

        logger.info(f"Pong enter view game_mode: {game_mode}")

        if not game_mode:
            return redirect("pong:selectmode")

        context["game_mode"] = game_mode
        context["GameMode"] = GameMode.as_dict()

        if game_mode == GameMode.TOURNAMENT.value:
            context["form"] = TournamentForm()
            context["tournaments"] = Tournament.objects.filter(is_active=True)
        else:
            context["form"] = PongRoomForm()
            context["rooms"] = PongRoom.objects.filter(
                game_mode=game_mode, is_active=True
            )
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/enter.html", self.get_context_data(**kwargs))
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        game_mode = kwargs.get("game_mode")

        logger.info(f"PongEnterView POST game_mode: {game_mode}")
        logger.info(f"PongEnterView POST data: {request.POST}")

        if game_mode == GameMode.TOURNAMENT.value:
            form = TournamentForm(request.POST)
            max_players = request.POST.get("max_players")
            if max_players in ["4", "8"] and form.is_valid():
                tournament = form.save(commit=False)
                tournament.max_players = int(max_players)
                tournament.save()
                return JsonResponse({"message":"sala criada"}, status=200)
                # return redirect("pong:pongtournament", tournament_id=tournament.id)
            else:
                context = self.get_context_data(**kwargs)
                context["form"] = form
                context["tournament_id"] = tournament.id
                context["game_mode"] = game_mode
                return self.render_to_response(context)
        else:
            form = PongRoomForm(request.POST)
            if form.is_valid():
                room = form.save(commit=False)
                room.game_mode = game_mode
                room.save()
                return HTTPResponse()
                # return redirect("pong:pongroom", room_id=room.id)
            else:
                context = self.get_context_data(**kwargs)
                context["form"] = form
                return self.render_to_response(context)


class PongRoomView(TemplateView):
    template_name = "pong/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = kwargs.get("room_id")
        try:
            room = PongRoom.objects.get(id=room_id)
            context["room"] = room
            context["game_mode"] = room.game_mode
        except PongRoom.DoesNotExist:
            context["room"] = None
            context["game_mode"] = None
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context["room"] is None:
            return redirect("pong:selectmode")
        return self.render_to_response(context)


class PongTournamentView(DetailView):
    model = Tournament
    template_name = "pong/tournament.html"
    context_object_name = "tournament"
    pk_url_kwarg = "tournament_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        participants = TournamentParticipant.objects.filter(tournament=tournament)
        matches = Match.objects.filter(
            room__game_mode=GameMode.TOURNAMENT.value,
        )
        context["participants"] = participants
        context["matches"] = matches
        context["game_mode"] = kwargs.get("game_mode")
        context["user"] = self.request.user
        logger.info(
            f"Displaying tournament: {tournament.name} with {participants.count()} participants and {matches.count()} matches"
        )
        return context

    def post(self, request, *args, **kwargs):
        # implementar lógica para inscrisão em torneio

        tournament = self.get_object()
        return redirect("pong:pongtournament", tournament_id=tournament.id)
