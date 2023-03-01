from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("view/<int:listing_id>", views.bid_view, name="view"),
    path("watch", views.watch, name="watch"),
    path("category", views.category, name="category"),
]
