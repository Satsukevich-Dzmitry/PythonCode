from django.views.generic import TemplateView


class IndexStyleView(TemplateView):
    template_name = "home/index.css"
    content_type = "text/css"