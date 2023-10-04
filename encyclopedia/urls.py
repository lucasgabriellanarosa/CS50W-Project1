from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name='search'),
    path("new_page", views.new_page, name='new_page'),
    path("edit_entry/<str:entry>", views.edit_entry, name='edit_entry'),
    path("delete_entry/<str:entry>", views.delete_entry, name='delete_entry'),
    path("random_entry", views.random_entry, name='random_entry'),
]
