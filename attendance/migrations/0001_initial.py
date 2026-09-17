from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Subject", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("name",models.CharField(max_length=120)),("code",models.CharField(blank=True,max_length=30)),("target_percentage",models.PositiveSmallIntegerField(default=75)),("color",models.CharField(default="#a78bfa",max_length=7)),("user",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="subjects",to=settings.AUTH_USER_MODEL))],options={"ordering":("name",)}),
        migrations.CreateModel(name="AttendanceRecord", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("date",models.DateField()),("present",models.BooleanField(default=True)),("note",models.CharField(blank=True,max_length=200)),("subject",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="records",to="attendance.subject"))],options={"ordering":("-date",)}),
        migrations.AddConstraint(model_name="attendancerecord",constraint=models.UniqueConstraint(fields=("subject","date"),name="unique_subject_attendance_date")),
    ]
