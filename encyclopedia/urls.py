from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.form, name="form"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("form_entry", views.new_entry_form, name="form_entry"),
    path("random", views.random_entry, name="random"),
]
