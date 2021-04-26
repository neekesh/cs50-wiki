from django.urls import path, reverse

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("save_page", views.save_page, name="save_page"),
    path('edit_page/<str:title>', views.edit, name="edit"),
    path('save_page/<str:title>', views.save_page, name="save_edited_page"),
    path('random_page', views.random_page, name="random_page")
]
