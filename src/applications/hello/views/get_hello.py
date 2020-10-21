from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.forms import HelloForm


class GreetView(FormView):
    form_class = HelloForm
    success_url = reverse_lazy("hello:index")
    template_name = "hello/hello.html"

    def form_valid(self, form):
        self.request.session["name"] = form.cleaned_data["name"]
        self.request.session["surname"] = form.cleaned_data["surname"]
        self.request.session["age"] = form.cleaned_data["age"]
        return super().form_valid(form)

    def get_initial(self):
        data = {
            "name": self.request.session.get("name"),
            "surname": self.request.session.get("surname"),
            "age": self.request.session.get("age"),
        }

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_name"] = self.request.session.get("name") or "Anon"
        context["user_surname"] = self.request.session.get("surname") or "No surname set"
        age = self.request.session.get("age")
        if age:
            context["user_year"] = datetime.now().year - age
        else:
            context["user_year"] = "Not set"
        return context
