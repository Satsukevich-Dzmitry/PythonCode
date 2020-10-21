from django.urls import path

from applications.snake.apps import SnakeConfig
from applications.snake.views import SnakeIndexView, SnakeScriptView

app_name = SnakeConfig.label

urlpatterns = [
    path("", SnakeIndexView.as_view(), name="snake"),
    path("snakescript/", SnakeScriptView.as_view(), name="snakescript"),
]