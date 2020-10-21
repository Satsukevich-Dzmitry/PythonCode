from django.views.generic import TemplateView


class SnakeScriptView(TemplateView):
    template_name = "snake/snake_script.js"
    content_type = "text/javascript"
