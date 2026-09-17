from django import forms
from .models import Category, Task


class StyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control" if not isinstance(field.widget, forms.CheckboxInput) else "form-check-input"


class TaskForm(StyledForm):
    class Meta:
        model = Task
        fields = ("title", "description", "category", "priority", "due_date")
        widgets = {"description": forms.Textarea(attrs={"rows": 3}), "due_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=user)


class CategoryForm(StyledForm):
    class Meta:
        model = Category
        fields = ("name", "color")
        widgets = {"color": forms.TextInput(attrs={"type": "color"})}
