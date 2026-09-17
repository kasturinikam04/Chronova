from django.contrib import admin
from .models import AnalyticsSnapshot, Assignment, CareerMilestone, CareerRoadmap, Notification, StudyPlan, StudyPlanItem, VivaQuestion, VivaSession


class StudyPlanItemInline(admin.TabularInline):
    model = StudyPlanItem
    extra = 0


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "exam_date", "daily_hours", "status")
    list_filter = ("status",)
    inlines = (StudyPlanItemInline,)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "due_date", "priority", "completed")
    list_filter = ("priority", "completed")


admin.site.register((VivaSession, VivaQuestion, CareerRoadmap, CareerMilestone, Notification, AnalyticsSnapshot))
