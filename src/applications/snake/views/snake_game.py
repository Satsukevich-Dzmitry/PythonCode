from django.views.generic import TemplateView


class SnakeIndexView(TemplateView):
    template_name = "snake/snake.html"