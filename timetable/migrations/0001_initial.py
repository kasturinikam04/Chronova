from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="TimetableEntry", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=120)), ("day", models.PositiveSmallIntegerField(choices=[(0,"Monday"),(1,"Tuesday"),(2,"Wednesday"),(3,"Thursday"),(4,"Friday"),(5,"Saturday"),(6,"Sunday")])), ("start_time", models.TimeField()), ("end_time", models.TimeField()), ("location", models.CharField(blank=True,max_length=120)), ("color", models.CharField(default="#22d3ee",max_length=7)), ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="timetable_entries",to=settings.AUTH_USER_MODEL))], options={"ordering":("day","start_time")})]
