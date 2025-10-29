from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="wiki"),
    path("new/", views.new, name="new"),
    path("apology/", views.apology, name="apology")
]
