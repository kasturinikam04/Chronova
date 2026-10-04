from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("planner", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="AcademicDocument", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("document_type", models.CharField(choices=[("timetable", "Timetable image"), ("syllabus", "Syllabus PDF"), ("notes", "Notes"), ("question_paper", "Question paper")], max_length=20)),
            ("title", models.CharField(max_length=180)), ("file", models.FileField(upload_to="academic-documents/%Y/%m/")),
            ("extracted_text", models.TextField(blank=True)), ("extraction_status", models.CharField(default="pending", max_length=20)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="academic_documents", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ("-created_at",)}),
        migrations.AddIndex(model_name="academicdocument", index=models.Index(fields=["user", "document_type", "created_at"], name="planner_aca_user_id_d2e0e3_idx")),
    ]
