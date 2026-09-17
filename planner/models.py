from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StudyPlan(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_plans")
    subject = models.ForeignKey("attendance.Subject", on_delete=models.CASCADE, related_name="study_plans")
    exam_date = models.DateField()
    daily_hours = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0.5), MaxValueValidator(16)])
    units = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("exam_date", "-created_at")
        indexes = [models.Index(fields=("user", "status", "exam_date"))]

    def __str__(self):
        return f"{self.subject} plan"


class StudyPlanItem(models.Model):
    class Energy(models.TextChoices):
        HIGH = "high", "High energy"
        MEDIUM = "medium", "Medium energy"
        LOW = "low", "Low energy"

    plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name="items")
    date = models.DateField()
    title = models.CharField(max_length=160)
    unit_number = models.PositiveSmallIntegerField()
    duration_minutes = models.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(720)])
    energy_level = models.CharField(max_length=10, choices=Energy.choices, default=Energy.MEDIUM)
    is_revision = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ("date", "unit_number")
        indexes = [models.Index(fields=("plan", "date", "completed"))]


class Assignment(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignments")
    subject = models.ForeignKey("attendance.Subject", on_delete=models.SET_NULL, null=True, blank=True, related_name="assignments")
    title = models.CharField(max_length=160)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("completed", "due_date")
        indexes = [models.Index(fields=("user", "completed", "due_date"))]


class VivaSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="viva_sessions")
    topic = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)


class VivaQuestion(models.Model):
    class Difficulty(models.TextChoices):
        FOUNDATION = "foundation", "Foundation"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    session = models.ForeignKey(VivaSession, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=500)
    suggested_answer = models.TextField()
    follow_up = models.CharField(max_length=500)
    difficulty = models.CharField(max_length=15, choices=Difficulty.choices)
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ("position",)


class CareerRoadmap(models.Model):
    class Path(models.TextChoices):
        PLACEMENT = "placement", "Placement"
        HIGHER_STUDIES = "higher_studies", "Higher studies"
        GOVERNMENT = "government", "Government exams"
        ENTREPRENEURSHIP = "entrepreneurship", "Entrepreneurship"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="career_roadmaps")
    path = models.CharField(max_length=20, choices=Path.choices)
    target_role = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "path"), name="unique_user_career_path")]


class CareerMilestone(models.Model):
    roadmap = models.ForeignKey(CareerRoadmap, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=180)
    detail = models.TextField()
    category = models.CharField(max_length=30, default="skill")
    position = models.PositiveSmallIntegerField()
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ("position",)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chronova_notifications")
    title = models.CharField(max_length=160)
    body = models.CharField(max_length=300)
    link = models.CharField(max_length=300, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("user", "read_at", "created_at"))]


class AnalyticsSnapshot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="analytics_snapshots")
    date = models.DateField()
    attendance_score = models.PositiveSmallIntegerField(default=0)
    task_completion_score = models.PositiveSmallIntegerField(default=0)
    study_minutes = models.PositiveIntegerField(default=0)
    productivity_score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("-date",)
        constraints = [models.UniqueConstraint(fields=("user", "date"), name="unique_user_analytics_date")]
