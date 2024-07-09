from typing import Sequence

from django.urls import path
from django.views.decorators.cache import cache_page

from .models import *
from . import views


app_name: str = 'blog'
urlpatterns: Sequence = [
    # ex: /blog/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /blog/articles
    path("articles/", views.ArticlesView.as_view(), name="articles"),
    # ex: /blog/article/1
    path("article/<int:pk>", cache_page(60)(views.DetailView.as_view()), name="detail"),
]
