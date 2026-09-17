# Generated manually for the Chronova foundation.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(
        name="Profile",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("full_name", models.CharField(max_length=150)),
            ("profile_picture", models.ImageField(blank=True, null=True, upload_to="profile_pictures/")),
            ("college_name", models.CharField(blank=True, max_length=200)),
            ("course_name", models.CharField(blank=True, max_length=150)),
            ("year_semester", models.CharField(blank=True, max_length=50, verbose_name="Year / semester")),
            ("career_goal", models.TextField(blank=True)),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
        ],
    )]
