from django.urls import path
from . import views

app_name = "planner"
urlpatterns = [
    path("", views.overview, name="overview"), path("study-plan/create/", views.study_plan_create, name="study_plan_create"),
    path("study-plan/<int:pk>/regenerate/", views.study_plan_regenerate, name="study_plan_regenerate"), path("study-item/<int:pk>/toggle/", views.study_item_toggle, name="study_item_toggle"),
    path("assignments/create/", views.assignment_create, name="assignment_create"), path("assignments/<int:pk>/toggle/", views.assignment_toggle, name="assignment_toggle"),
    path("viva/create/", views.viva_create, name="viva_create"), path("career/create/", views.career_create, name="career_create"),
    path("notifications/read/", views.notifications_read, name="notifications_read"),
]
