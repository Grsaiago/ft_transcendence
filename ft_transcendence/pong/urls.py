from django.urls import path

from . import views

app_name = "pong"
urlpatterns = [
    path("enter/", views.PongEnterView.as_view(), name="pongenter"),
    path("room/<int:room_id>/", views.PongRoomView.as_view(), name="pongroom"),
]
