from django.views.generic import TemplateView


class PongView(TemplateView):
    template_name = "pong/pong.html"
