from django import forms
from django.utils import timezone
from .models import Assignment, CareerRoadmap, StudyPlan


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
