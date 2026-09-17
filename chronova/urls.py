from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("preferences/", include("preferences.urls")),
    path("tasks/", include("tasks.urls")),
    path("timetable/", include("timetable.urls")),
    path("attendance/", include("attendance.urls")),
    path("planner/", include("planner.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
