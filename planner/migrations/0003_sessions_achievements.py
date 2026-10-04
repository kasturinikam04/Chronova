from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("planner", "0002_academic_document"), migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("attendance", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Achievement", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("code", models.SlugField(unique=True)), ("name", models.CharField(max_length=100)), ("description", models.CharField(max_length=240)), ("threshold", models.PositiveSmallIntegerField(default=1))]),
        migrations.CreateModel(name="StudySession", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("started_at", models.DateTimeField()), ("ended_at", models.DateTimeField()), ("note", models.CharField(blank=True, max_length=240)), ("created_at", models.DateTimeField(auto_now_add=True)), ("subject", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="study_sessions", to="attendance.subject")), ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="study_sessions", to=settings.AUTH_USER_MODEL))], options={"ordering": ("-started_at",)}),
        migrations.CreateModel(name="UserAchievement", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("earned_at", models.DateTimeField(auto_now_add=True)), ("achievement", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="earners", to="planner.achievement")), ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="achievements", to=settings.AUTH_USER_MODEL))]),
        migrations.AddIndex(model_name="studysession", index=models.Index(fields=["user", "started_at"], name="planner_stu_user_id_1f80f2_idx")),
        migrations.AddConstraint(model_name="userachievement", constraint=models.UniqueConstraint(fields=("user", "achievement"), name="unique_user_achievement")),
    ]
