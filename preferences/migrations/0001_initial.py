# Generated manually for the Chronova foundation.
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(
        name="Preference",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("wake_up_time", models.TimeField(blank=True, null=True)),
            ("sleep_time", models.TimeField(blank=True, null=True)),
            ("preferred_study_hours", models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(24)])),
            ("preferred_study_time", models.CharField(blank=True, choices=[("morning", "Morning"), ("afternoon", "Afternoon"), ("evening", "Evening"), ("night", "Night")], max_length=20)),
            ("daily_available_hours", models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(24)])),
            ("academic_goal", models.TextField(blank=True)),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="preferences", to=settings.AUTH_USER_MODEL)),
        ],
    )]
