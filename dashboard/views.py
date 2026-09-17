from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import Profile
from preferences.models import Preference
from attendance.models import Subject
from tasks.models import Task
from timetable.models import TimetableEntry
from django.utils import timezone


@login_required
def home(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={"full_name": request.user.get_full_name()})
    preferences, _ = Preference.objects.get_or_create(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    subjects = Subject.objects.filter(user=request.user).prefetch_related("records")
    today = timezone.localdate()
    return render(request, "dashboard/home.html", {
        "profile": profile, "preferences": preferences,
        "task_total": tasks.count(), "task_complete": tasks.filter(completed=True).count(),
        "upcoming_tasks": tasks.filter(completed=False).filter(due_date__gte=today).order_by("due_date")[:4],
        "timetable_count": TimetableEntry.objects.filter(user=request.user).count(),
        "subjects": subjects, "attendance_average": round(sum(subject.percentage for subject in subjects) / subjects.count(), 1) if subjects else 0,
    })
