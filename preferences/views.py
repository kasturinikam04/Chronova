from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import PreferenceForm
from .models import Preference


@login_required
def edit(request):
    preferences, _ = Preference.objects.get_or_create(user=request.user)
    form = PreferenceForm(request.POST or None, instance=preferences)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your study preferences have been updated.")
        return redirect("dashboard:home")
    return render(request, "preferences/form.html", {"form": form})
