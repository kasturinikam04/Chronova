from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        name_parts = self.cleaned_data["full_name"].strip().split(maxsplit=1)
        user.first_name = name_parts[0] if name_parts else ""
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        if commit:
            user.save()
            Profile.objects.filter(user=user).update(full_name=self.cleaned_data["full_name"].strip())
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("full_name", "profile_picture", "college_name", "course_name", "year_semester", "career_goal")
        widgets = {"career_goal": forms.Textarea(attrs={"rows": 3})}
