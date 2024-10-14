from django.views.generic import TemplateView


class PongEnter(TemplateView):
    template_name = "pong/enter.html"
