from django.views.generic import TemplateView


class hellocss(TemplateView):
    template_name = "hello/hellodark.css"
    content_type = "text/css"