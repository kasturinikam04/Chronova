from django.conf import settings
from django.db import models


class Subject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, blank=True)
    target_percentage = models.PositiveSmallIntegerField(default=75)
    color = models.CharField(max_length=7, default="#a78bfa")

    class Meta:
        ordering = ("name",)

    @property
    def percentage(self):
        total = self.records.count()
        return round((self.records.filter(present=True).count() / total * 100), 1) if total else 0

    def __str__(self): return self.name


class AttendanceRecord(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="records")
    date = models.DateField()
    present = models.BooleanField(default=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ("-date",)
        constraints = [models.UniqueConstraint(fields=("subject", "date"), name="unique_subject_attendance_date")]
