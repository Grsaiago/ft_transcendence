from django.urls import path

from . import views

app_name = "pong"
urlpatterns = [
    path("play/", views.PongSelectGameMode.as_view(), name="selectmode"),
    path("enter/<str:game_mode>/", views.PongEnterView.as_view(), name="pongenter"),
    path("room/<int:room_id>/", views.PongRoomView.as_view(), name="pongroom"),
    path(
        "tournament/<int:tournament_id>/",
        views.PongTournamentView.as_view(),
        name="pongtournament",
    ),
]
