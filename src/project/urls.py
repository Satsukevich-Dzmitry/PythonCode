"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import json
from datetime import datetime
from pathlib import Path

from django.contrib import admin
from django.http import HttpResponse, HttpRequest
from django.urls import path, include


def index(request: HttpRequest):
    index_html = Path(__file__).parent.parent.parent/"html_files"/"index.html"
    with index_html.open("r") as f:
        content = f.read()
    return HttpResponse(content)



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("applications.home.urls")),
    path("hello/", include("applications.hello.urls")),
    path("snake/", include("applications.snake.urls")),
    path("blog/", include("applications.blog.urls"))
]
