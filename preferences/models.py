from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Preference(models.Model):
    STUDY_TIME_CHOICES = [("morning", "Morning"), ("afternoon", "Afternoon"), ("evening", "Evening"), ("night", "Night")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")
    wake_up_time = models.TimeField(blank=True, null=True)
    sleep_time = models.TimeField(blank=True, null=True)
    preferred_study_hours = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(24)])
    preferred_study_time = models.CharField(max_length=20, choices=STUDY_TIME_CHOICES, blank=True)
    daily_available_hours = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(24)])
    academic_goal = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"
