from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import Profile
from preferences.models import Preference
from attendance.models import Subject
from tasks.models import Task
from timetable.models import TimetableEntry
from planner.models import AcademicDocument, StudyPlan
from django.utils import timezone
from .intelligence import academic_health, daily_briefing, task_rank, weekly_insights


@login_required
def home(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={"full_name": request.user.get_full_name()})
    preferences, _ = Preference.objects.get_or_create(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    subjects = Subject.objects.filter(user=request.user).prefetch_related("records")
    today = timezone.localdate()
    assistant_question = request.POST.get("question", "").strip() if request.method == "POST" else ""
    from .intelligence import answer_assistant
    return render(request, "dashboard/home.html", {
        "profile": profile, "preferences": preferences,
        "task_total": tasks.count(), "task_complete": tasks.filter(completed=True).count(),
        "upcoming_tasks": tasks.filter(completed=False).filter(due_date__gte=today).order_by("due_date")[:4],
        "timetable_count": TimetableEntry.objects.filter(user=request.user).count(),
        "subjects": subjects, "attendance_average": round(sum(subject.percentage for subject in subjects) / subjects.count(), 1) if subjects else 0,
        "daily_briefing": daily_briefing(request.user), "academic_health": academic_health(request.user),
        "priority_tasks": [(task, task_rank(task, today)) for task in tasks.filter(completed=False).order_by("due_date")[:5]],
        "assistant_question": assistant_question, "assistant_answer": answer_assistant(request.user, assistant_question) if assistant_question else "",
        "weekly_insights": weekly_insights(request.user),
    })


@login_required
def search(request):
    query = request.GET.get("q", "").strip()
    results = []
    if query:
        for task in Task.objects.filter(user=request.user, title__icontains=query)[:8]: results.append(("Task", task.title, "tasks:list"))
        for subject in Subject.objects.filter(user=request.user, name__icontains=query)[:8]: results.append(("Subject", subject.name, "attendance:overview"))
        for entry in TimetableEntry.objects.filter(user=request.user, title__icontains=query)[:8]: results.append(("Timetable", entry.title, "timetable:schedule"))
        for plan in StudyPlan.objects.filter(user=request.user, subject__name__icontains=query).select_related("subject")[:8]: results.append(("Study plan", plan.subject.name, "planner:overview"))
        for document in AcademicDocument.objects.filter(user=request.user, title__icontains=query)[:8]: results.append(("Document", document.title, "planner:documents"))
    return render(request, "dashboard/search.html", {"query": query, "results": results})
