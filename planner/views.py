from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from attendance.models import Subject
from tasks.models import Task
from .forms import AssignmentForm, CareerRoadmapForm, StudyPlanForm, VivaForm
from .models import Assignment, CareerRoadmap, Notification, StudyPlan, StudyPlanItem, VivaSession
from .services import generate_career_milestones, generate_study_items, generate_viva_questions


def _health(user):
    subjects = Subject.objects.filter(user=user).prefetch_related("records")
    attendance = round(sum(s.percentage for s in subjects) / subjects.count()) if subjects else 0
    tasks = Task.objects.filter(user=user)
    task_score = round(tasks.filter(completed=True).count() / tasks.count() * 100) if tasks.exists() else 0
    assignments = Assignment.objects.filter(user=user)
    assignment_score = round(assignments.filter(completed=True).count() / assignments.count() * 100) if assignments.exists() else 0
    return {"attendance": attendance, "tasks": task_score, "assignments": assignment_score, "score": round((attendance + task_score + assignment_score) / 3)}


@login_required
def overview(request):
    today = timezone.localdate()
    plans = StudyPlan.objects.filter(user=request.user, status=StudyPlan.Status.ACTIVE).select_related("subject").prefetch_related("items")
    assignments = Assignment.objects.filter(user=request.user).select_related("subject")
    notification_query = Notification.objects.filter(user=request.user)
    unread_notifications = notification_query.filter(read_at__isnull=True).count()
    notifications = notification_query[:5]
    planned_minutes = StudyPlanItem.objects.filter(plan__user=request.user, date=today, completed=False).aggregate(total=Sum("duration_minutes"))["total"] or 0
    incomplete = Task.objects.filter(user=request.user, completed=False, due_date__lt=today).count()
    return render(request, "planner/overview.html", {
        "health": _health(request.user), "plans": plans, "assignments": assignments[:6], "overdue_assignments": assignments.filter(completed=False, due_date__lt=today).count(),
        "today_items": StudyPlanItem.objects.filter(plan__user=request.user, date=today).select_related("plan__subject"), "planned_minutes": planned_minutes,
        "incomplete_tasks": incomplete, "notifications": notifications, "unread_notifications": unread_notifications,
        "study_plan_form": StudyPlanForm(user=request.user), "assignment_form": AssignmentForm(user=request.user), "viva_form": VivaForm(), "career_form": CareerRoadmapForm(),
        "roadmaps": CareerRoadmap.objects.filter(user=request.user).prefetch_related("milestones"),
    })


@login_required
def study_plan_create(request):
    form = StudyPlanForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        plan = form.save(commit=False); plan.user = request.user; plan.save(); generate_study_items(plan)
        messages.success(request, "Your study plan is ready. It balances learning and revision through your exam date.")
    return redirect("planner:overview")


@login_required
def study_plan_regenerate(request, pk):
    plan = get_object_or_404(StudyPlan, pk=pk, user=request.user)
    if request.method == "POST":
        generate_study_items(plan); messages.success(request, "Plan regenerated with a fresh daily sequence.")
    return redirect("planner:overview")


@login_required
def study_item_toggle(request, pk):
    item = get_object_or_404(StudyPlanItem, pk=pk, plan__user=request.user)
    if request.method == "POST":
        item.completed = not item.completed; item.save(update_fields=("completed",))
    return redirect("planner:overview")


@login_required
def assignment_create(request):
    form = AssignmentForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        assignment = form.save(commit=False); assignment.user = request.user; assignment.save()
        messages.success(request, "Assignment added to your deadline radar.")
    return redirect("planner:overview")


@login_required
def assignment_toggle(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == "POST":
        assignment.completed = not assignment.completed
        assignment.completed_at = timezone.now() if assignment.completed else None
        assignment.save(update_fields=("completed", "completed_at"))
    return redirect("planner:overview")


@login_required
def viva_create(request):
    form = VivaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        session = VivaSession.objects.create(user=request.user, topic=form.cleaned_data["topic"])
        generate_viva_questions(session)
        messages.success(request, f"Five viva questions were generated for {session.topic}.")
    return redirect("planner:overview")


@login_required
def career_create(request):
    form = CareerRoadmapForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        roadmap = form.save(commit=False); roadmap.user = request.user
        CareerRoadmap.objects.filter(user=request.user, path=roadmap.path).delete()
        roadmap.save(); generate_career_milestones(roadmap)
        messages.success(request, "Your career roadmap is ready to explore.")
    return redirect("planner:overview")


@login_required
def notifications_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, read_at__isnull=True).update(read_at=timezone.now())
    return redirect("planner:overview")
