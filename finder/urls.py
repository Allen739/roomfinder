from django.urls import path
from . import views

app_name = "finder"

urlpatterns = [
    path("search/", views.search_rooms, name="search_rooms"),
    path("", views.upload_excel, name="upload_excel"),
]
