from django.contrib import admin
from .models import AttendanceRecord, Subject
admin.site.register(Subject)
admin.site.register(AttendanceRecord)
