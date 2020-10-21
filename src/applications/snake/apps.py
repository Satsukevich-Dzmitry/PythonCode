from django.apps import AppConfig


class SnakeConfig(AppConfig):
    label = "snake"
    name = f"applications.{label}"
