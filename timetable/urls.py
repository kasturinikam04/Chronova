from django.urls import path
from . import views
app_name = "timetable"
urlpatterns = [path("", views.schedule, name="schedule"), path("create/", views.entry_create, name="create"), path("<int:pk>/edit/", views.entry_edit, name="edit"), path("<int:pk>/delete/", views.entry_delete, name="delete")]
