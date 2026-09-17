from django import forms
from .models import Preference


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ("wake_up_time", "sleep_time", "preferred_study_hours", "preferred_study_time", "daily_available_hours", "academic_goal")
        widgets = {
            "wake_up_time": forms.TimeInput(attrs={"type": "time"}),
            "sleep_time": forms.TimeInput(attrs={"type": "time"}),
            "academic_goal": forms.Textarea(attrs={"rows": 3}),
        }
