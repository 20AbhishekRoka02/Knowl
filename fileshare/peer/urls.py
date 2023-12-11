from django.urls import include, path
from . import views
urlpatterns = [
    path("search/", views.search_peer, name="search"),
    path("share/", views.share, name="share"),
    path("filesupload/", views.uploadfiles, name="filesupload")
]
