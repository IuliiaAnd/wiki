from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("create_entry/", views.create_new_entry, name="create_entry"),
    path("edit/<str:title>", views.edit_content, name='edit_content'),
    path("random_page", views.random_page, name="random_page"),
]
