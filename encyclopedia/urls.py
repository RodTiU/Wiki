from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.form, name="form"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("form_entry", views.new_entry_form, name="form_entry"),
    path("edit/<str:title>", views.edit_redirector, name="edit"),
    path("form_edit", views.send_edit_form, name="form_edit"),
    path("random", views.random_entry, name="random"),
]
