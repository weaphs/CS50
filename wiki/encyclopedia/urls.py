from django.urls import path

from . import views
from .util import list_entries

titles=list_entries()

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search_results", views.search, name="search"),
    path("wiki/create_page_form", views.create_page_form, name="create_page_form"),
    path("wiki/create_page", views.create_page, name="create_page"),
    path("wiki/random_page", views.random_page, name="random_page"),
    path("wiki/<str:title>/edit_page", views.edit_page, name="edit_page"),
    path("wiki/<str:title>/save_edit/", views.save_edit, name="save_edit"),
    path("wiki/<str:title>/", views.wiki_page, name="wiki_page")

]
