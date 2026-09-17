from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, RegistrationForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to Chronova. Your account is ready.")
        return redirect("dashboard:home")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={"full_name": request.user.get_full_name()})
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("dashboard:home")
    return render(request, "accounts/profile_form.html", {"form": form})
