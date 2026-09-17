from django.contrib import admin
from .models import Category, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "priority", "due_date", "completed")
    list_filter = ("priority", "completed")
    search_fields = ("title", "user__username")


admin.site.register(Category)
