from django.urls import path

from . import views

app_name = "pong"
urlpatterns = [
    path("enter/", views.PongEnter.as_view(), name="pongenter"),
]
