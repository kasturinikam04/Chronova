from django.conf import settings
from django.db import models


class TimetableEntry(models.Model):
    class Day(models.IntegerChoices):
        MONDAY = 0, "Monday"; TUESDAY = 1, "Tuesday"; WEDNESDAY = 2, "Wednesday"; THURSDAY = 3, "Thursday"; FRIDAY = 4, "Friday"; SATURDAY = 5, "Saturday"; SUNDAY = 6, "Sunday"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="timetable_entries")
    title = models.CharField(max_length=120)
    day = models.PositiveSmallIntegerField(choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=120, blank=True)
    color = models.CharField(max_length=7, default="#22d3ee")

    class Meta:
        ordering = ("day", "start_time")

    def __str__(self):
        return f"{self.get_day_display()}: {self.title}"
