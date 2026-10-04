"""Data-aware recommendations. Provider adapters can replace these rules later."""
from datetime import timedelta
from django.utils import timezone
from attendance.models import Subject
from planner.models import Assignment, StudyPlan, StudyPlanItem
from tasks.models import Task
from timetable.models import TimetableEntry


def task_rank(task, today=None):
    today = today or timezone.localdate()
    if task.due_date:
        days = (task.due_date - today).days
        if days <= 1 or (task.priority == Task.Priority.HIGH and days <= 3):
            return "critical"
        if days <= 7 or task.priority == Task.Priority.HIGH:
            return "important"
    return "normal"


def attendance_intelligence(user):
    insights = []
    for subject in Subject.objects.filter(user=user).prefetch_related("records"):
        total = subject.records.count()
        present = subject.records.filter(present=True).count()
        target = subject.target_percentage / 100
        percentage = subject.percentage
        safe_misses = max(0, int((present / target) - total)) if target else 0
        recover_classes = max(0, int((target * total - present) / (1 - target) + .999)) if target and percentage < subject.target_percentage else 0
        insights.append({"subject": subject, "percentage": percentage, "safe_misses": safe_misses, "recover_classes": recover_classes, "at_risk": total > 0 and percentage < subject.target_percentage})
    health = round(sum(item["percentage"] for item in insights) / len(insights)) if insights else 0
    return {"score": health, "subjects": insights, "at_risk": [item for item in insights if item["at_risk"]]}


def daily_briefing(user):
    today = timezone.localdate()
    tasks = Task.objects.filter(user=user, completed=False)
    assignments = Assignment.objects.filter(user=user, completed=False)
    exams = StudyPlan.objects.filter(user=user, status=StudyPlan.Status.ACTIVE, exam_date__gte=today).select_related("subject")
    attendance = attendance_intelligence(user)
    ranked = sorted(tasks, key=lambda item: ({"critical": 0, "important": 1, "normal": 2}[task_rank(item, today)], item.due_date or today + timedelta(days=365)))
    lines = []
    if tasks.exists(): lines.append(f"You have {tasks.count()} pending task{'s' if tasks.count() != 1 else ''}.")
    if assignments.exists(): lines.append(f"{assignments.count()} assignment{'s are' if assignments.count() != 1 else ' is'} still open.")
    next_exam = exams.first()
    if next_exam: lines.append(f"{next_exam.subject.name} exam is in {(next_exam.exam_date - today).days} day{'s' if (next_exam.exam_date - today).days != 1 else ''}.")
    if attendance["at_risk"]: lines.append(f"Attendance needs attention in {attendance['at_risk'][0]['subject'].name}.")
    recommendation = f"Complete {ranked[0].title} today." if ranked else ("Use your next free slot for revision." if next_exam else "Your system is clear—protect one focused study block today.")
    return {"summary": " ".join(lines) or "Add your classes, tasks, and study plan to unlock a personalised briefing.", "recommendation": recommendation}


def timetable_analysis(user):
    entries = TimetableEntry.objects.filter(user=user)
    result = []
    for day, label in TimetableEntry.Day.choices:
        day_entries = list(entries.filter(day=day).order_by("start_time"))
        busy_minutes = sum((entry.end_time.hour * 60 + entry.end_time.minute) - (entry.start_time.hour * 60 + entry.start_time.minute) for entry in day_entries)
        free_minutes = max(0, 8 * 60 - busy_minutes)
        result.append({"day": label, "free_hours": round(free_minutes / 60, 1), "overloaded": busy_minutes >= 6 * 60, "underutilized": busy_minutes <= 2 * 60})
    best = max(result, key=lambda item: item["free_hours"])
    return {"days": result, "recommendation": f"{best['day']} has about {best['free_hours']} free hours—reserve one block for revision or an important task."}


def academic_health(user):
    attendance = attendance_intelligence(user)["score"]
    tasks = Task.objects.filter(user=user)
    completion = round(tasks.filter(completed=True).count() / tasks.count() * 100) if tasks.exists() else 50
    upcoming = StudyPlan.objects.filter(user=user, status=StudyPlan.Status.ACTIVE, exam_date__gte=timezone.localdate()).count()
    readiness = max(40, 100 - upcoming * 10)
    score = round(attendance * .4 + completion * .35 + readiness * .25)
    label = "Excellent" if score >= 80 else "Good" if score >= 60 else "Needs attention"
    return {"score": score, "label": label, "reasons": [f"Attendance contributes {round(attendance)} points of evidence.", f"Task completion is {completion}%.", f"{upcoming} active exam plan{'s' if upcoming != 1 else ''} need attention."]}


def weekly_insights(user):
    start = timezone.localdate() - timedelta(days=6)
    items = StudyPlanItem.objects.filter(plan__user=user, date__gte=start).select_related("plan__subject")
    by_subject = {}
    by_day = {}
    for item in items:
        by_subject[item.plan.subject.name] = by_subject.get(item.plan.subject.name, 0) + item.duration_minutes
        by_day[item.date.strftime("%A")] = by_day.get(item.date.strftime("%A"), 0) + item.duration_minutes
    most = max(by_subject, key=by_subject.get) if by_subject else "No study sessions logged"
    best_day = max(by_day, key=by_day.get) if by_day else "No study day yet"
    missed = Task.objects.filter(user=user, completed=False, due_date__lt=timezone.localdate()).count()
    return {"most_studied": most, "best_day": best_day, "missed_deadlines": missed}


def answer_assistant(user, question):
    query = question.lower()
    briefing = daily_briefing(user)
    attendance = attendance_intelligence(user)
    if "attendance" in query or "weak" in query:
        at_risk = attendance["at_risk"]
        return f"Your attendance health is {attendance['score']}%. " + (f"{at_risk[0]['subject'].name} is currently at risk at {at_risk[0]['percentage']}%." if at_risk else "No tracked subject is below its target.")
    if "assignment" in query or "pending" in query:
        open_assignments = Assignment.objects.filter(user=user, completed=False).order_by("due_date")
        return f"You have {open_assignments.count()} pending assignments." + (f" Start with {open_assignments.first().title}, due {open_assignments.first().due_date:%b %d}." if open_assignments else "")
    if "study" in query or "today" in query:
        return briefing["recommendation"]
    return briefing["summary"] + " " + briefing["recommendation"]
