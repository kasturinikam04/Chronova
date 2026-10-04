from django import forms
from django.utils import timezone
from .models import AcademicDocument, Assignment, CareerRoadmap, StudyPlan, StudySession


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class StudyPlanForm(StyledModelForm):
    class Meta:
        model = StudyPlan
        fields = ("subject", "units", "exam_date", "daily_hours")
        widgets = {"exam_date": forms.DateInput(attrs={"type": "date"}), "daily_hours": forms.NumberInput(attrs={"step": "0.5"})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = self.fields["subject"].queryset.filter(user=user)

    def clean_exam_date(self):
        exam_date = self.cleaned_data["exam_date"]
        if exam_date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future exam date.")
        return exam_date


class AssignmentForm(StyledModelForm):
    class Meta:
        model = Assignment
        fields = ("title", "subject", "due_date", "priority", "notes")
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"}), "notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = self.fields["subject"].queryset.filter(user=user)


class VivaForm(forms.Form):
    topic = forms.CharField(max_length=180, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Operating system scheduling"}))


class CareerRoadmapForm(StyledModelForm):
    class Meta:
        model = CareerRoadmap
        fields = ("path", "target_role")


class DocumentUploadForm(StyledModelForm):
    class Meta:
        model = AcademicDocument
        fields = ("document_type", "title", "file")

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        allowed = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
        extension = "." + uploaded.name.rsplit(".", 1)[-1].lower() if "." in uploaded.name else ""
        if extension not in allowed:
            raise forms.ValidationError("Upload a PDF or a supported image file.")
        if uploaded.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Files must be 10 MB or smaller.")
        return uploaded


class StudySessionForm(StyledModelForm):
    class Meta:
        model = StudySession
        fields = ("subject", "started_at", "ended_at", "note")
        widgets = {"started_at": forms.DateTimeInput(attrs={"type": "datetime-local"}), "ended_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = self.fields["subject"].queryset.filter(user=user)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("started_at") and cleaned.get("ended_at") and cleaned["ended_at"] <= cleaned["started_at"]:
            self.add_error("ended_at", "End time must be after the start time.")
        return cleaned
