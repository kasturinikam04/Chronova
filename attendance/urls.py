from django.urls import path
from . import views
app_name = "attendance"
urlpatterns = [path("", views.overview, name="overview"), path("subjects/create/", views.subject_create, name="subject_create"), path("records/create/", views.record_create, name="record_create")]
