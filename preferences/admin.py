from django.contrib import admin
from .models import Preference


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "preferred_study_time", "preferred_study_hours", "daily_available_hours")
    list_select_related = ("user",)
