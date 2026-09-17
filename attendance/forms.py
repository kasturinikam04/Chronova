from django import forms
from .models import AttendanceRecord, Subject


class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.widget.attrs["class"] = "form-control" if not isinstance(field.widget, forms.CheckboxInput) else "form-check-input"


class SubjectForm(BaseStyledForm):
    class Meta:
        model = Subject
        fields = ("name", "code", "target_percentage", "color")
        widgets = {"color": forms.TextInput(attrs={"type": "color"})}


class AttendanceRecordForm(BaseStyledForm):
    class Meta:
        model = AttendanceRecord
        fields = ("subject", "date", "present", "note")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.filter(user=user)
