from django.urls import path

from . import views

app_name = "pong"
urlpatterns = [
    path("pong/", views.PongView.as_view(), name="pong"),
]
