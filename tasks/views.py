from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CategoryForm, TaskForm
from .models import Category, Task


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).select_related("category")
    categories = Category.objects.filter(user=request.user)
    return render(request, "tasks/list.html", {"tasks": tasks, "categories": categories, "form": TaskForm(user=request.user), "category_form": CategoryForm()})


@login_required
def task_create(request):
    form = TaskForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False); task.user = request.user; task.save()
        messages.success(request, "Task added to your focus list.")
    return redirect("tasks:list")


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Task updated.")
        return redirect("tasks:list")
    return render(request, "tasks/form.html", {"form": form, "task": task})


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.completed = not task.completed
        task.completed_at = timezone.now() if task.completed else None
        task.save(update_fields=("completed", "completed_at", "updated_at"))
    return redirect("tasks:list")


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete(); messages.success(request, "Task deleted.")
    return redirect("tasks:list")


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        category = form.save(commit=False); category.user = request.user; category.save()
        messages.success(request, "Category created.")
    return redirect("tasks:list")
