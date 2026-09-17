from datetime import timedelta
from django.utils import timezone
from .models import CareerMilestone, StudyPlanItem, VivaQuestion


def generate_study_items(plan):
    """Deterministic first-party planner; can be swapped for an AI provider later."""
    plan.items.all().delete()
    today = timezone.localdate()
    days = max((plan.exam_date - today).days, 1)
    daily_minutes = int(float(plan.daily_hours) * 60)
    items = []
    for offset in range(days):
        day = today + timedelta(days=offset)
        revision = offset >= max(days - min(7, max(2, days // 4)), 1)
        unit = (offset % plan.units) + 1
        energy = [StudyPlanItem.Energy.HIGH, StudyPlanItem.Energy.MEDIUM, StudyPlanItem.Energy.LOW][offset % 3]
        title = f"{'Revise' if revision else 'Learn'} unit {unit}"
        items.append(StudyPlanItem(plan=plan, date=day, title=title, unit_number=unit, duration_minutes=daily_minutes, energy_level=energy, is_revision=revision))
    StudyPlanItem.objects.bulk_create(items)


def generate_viva_questions(session):
    topic = session.topic
    templates = [
        ("Foundation", f"What is {topic}?", f"Define {topic} clearly, then name its core purpose and context.", f"Which term is most closely related to {topic}?"),
        ("Foundation", f"Why is {topic} important?", f"Explain the practical problem it solves and its key benefit.", f"Who typically uses it?"),
        ("Intermediate", f"What are the main components of {topic}?", f"Break the topic into its important parts and describe how they connect.", f"Which component is most critical, and why?"),
        ("Intermediate", f"How would you apply {topic} in a real scenario?", f"Use a concise example: situation, approach, and expected outcome.", f"What could go wrong in that scenario?"),
        ("Advanced", f"What are the limitations of {topic}?", f"Discuss trade-offs, assumptions, and when an alternative may be better.", f"How would you reduce one limitation?"),
    ]
    VivaQuestion.objects.bulk_create([VivaQuestion(session=session, difficulty=d.lower(), question=q, suggested_answer=a, follow_up=f, position=i) for i, (d, q, a, f) in enumerate(templates, 1)])


def generate_career_milestones(roadmap):
    roadmaps = {
        "placement": [("Foundation skills", "Choose the technical foundations expected for your target role.", "skill"), ("Portfolio project", "Build and document one role-relevant project with a clear outcome.", "project"), ("Interview practice", "Schedule weekly aptitude, technical, and communication practice.", "practice")],
        "higher_studies": [("Program research", "Shortlist programs based on curriculum, faculty, and eligibility.", "research"), ("Exam preparation", "Create a focused preparation cycle for entrance requirements.", "practice"), ("Application portfolio", "Prepare your statement, references, and academic evidence.", "application")],
        "government": [("Exam blueprint", "Map the syllabus, eligibility, and exam calendar.", "research"), ("Core preparation", "Build a consistent daily cycle across the highest-weight subjects.", "practice"), ("Mock analysis", "Review every mock for concepts and timing gaps.", "practice")],
        "entrepreneurship": [("Problem discovery", "Talk to potential users and document the problem worth solving.", "research"), ("Prototype", "Build the smallest testable version of your idea.", "project"), ("Launch experiment", "Run a small launch, measure feedback, and iterate.", "practice")],
    }
    roadmap.milestones.all().delete()
    CareerMilestone.objects.bulk_create([CareerMilestone(roadmap=roadmap, title=t, detail=d, category=c, position=i) for i, (t, d, c) in enumerate(roadmaps[roadmap.path], 1)])
