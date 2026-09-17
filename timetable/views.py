from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TimetableEntryForm
from .models import TimetableEntry


@login_required
def schedule(request):
    entries = TimetableEntry.objects.filter(user=request.user)
    grouped = {day: entries.filter(day=number) for number, day in TimetableEntry.Day.choices}
    return render(request, "timetable/schedule.html", {"grouped": grouped, "form": TimetableEntryForm(), "today": date.today().weekday()})


@login_required
def entry_create(request):
    form = TimetableEntryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False); entry.user = request.user; entry.save()
        messages.success(request, "Timetable entry created.")
    return redirect("timetable:schedule")


@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(TimetableEntry, pk=pk, user=request.user)
    form = TimetableEntryForm(request.POST or None, instance=entry)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Timetable entry updated.")
        return redirect("timetable:schedule")
    return render(request, "timetable/form.html", {"form": form, "entry": entry})


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(TimetableEntry, pk=pk, user=request.user)
    if request.method == "POST": entry.delete(); messages.success(request, "Timetable entry deleted.")
    return redirect("timetable:schedule")
