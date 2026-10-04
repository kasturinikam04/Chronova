from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("planner", "0003_sessions_achievements")]
    operations = [migrations.CreateModel(name="DocumentAnalysis", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("topics", models.JSONField(default=list)), ("summary", models.TextField(blank=True)), ("priority_score", models.PositiveSmallIntegerField(default=0)), ("updated_at", models.DateTimeField(auto_now=True)), ("document", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="analysis", to="planner.academicdocument"))])]
