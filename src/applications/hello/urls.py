from django.urls import path

from applications.hello.apps import HelloConfig
from applications.hello.views import GreetView, ResetView, hellocss

app_name = HelloConfig.label

urlpatterns = [
    path("", GreetView.as_view(), name="index"),
    path("update/", GreetView.as_view(), name="update"),
    path("reset/", ResetView.as_view(), name="reset"),
    path("style/", hellocss.as_view(), name="hellocss"),
]


