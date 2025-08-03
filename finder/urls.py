from django.urls import path
from . import views, api

app_name = "finder"

urlpatterns = [
    path("search/", views.search_rooms, name="search_rooms"),
    path("upload/", views.upload_excel, name="upload_excel"),
    path("api/room/<int:room_id>/", api.room_details, name="room_details"),
    path("", views.home, name="home"),
]
