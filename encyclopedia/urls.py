from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.form, name="form"),
    # path("new_entry", views.newpage, name="new_entry"),
]
