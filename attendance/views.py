from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import AttendanceRecordForm, SubjectForm
from .models import Subject


@login_required
def overview(request):
    subjects = Subject.objects.filter(user=request.user).prefetch_related("records")
    return render(request, "attendance/overview.html", {"subjects": subjects, "subject_form": SubjectForm(), "record_form": AttendanceRecordForm(user=request.user)})


@login_required
def subject_create(request):
    form = SubjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        subject = form.save(commit=False); subject.user = request.user; subject.save(); messages.success(request, "Subject added.")
    return redirect("attendance:overview")


@login_required
def record_create(request):
    form = AttendanceRecordForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Attendance record saved.")
    return redirect("attendance:overview")
