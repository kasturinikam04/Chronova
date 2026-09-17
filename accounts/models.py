from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    college_name = models.CharField(max_length=200, blank=True)
    course_name = models.CharField(max_length=150, blank=True)
    year_semester = models.CharField(max_length=50, blank=True, verbose_name="Year / semester")
    career_goal = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name or self.user.username}'s profile"
