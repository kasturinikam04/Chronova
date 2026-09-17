from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class PreferencesTests(TestCase):
    def test_authenticated_user_can_save_preferences(self):
        user = User.objects.create_user("student", "student@example.com", "Strong-pass-2026!")
        self.client.force_login(user)
        response = self.client.post(reverse("preferences:edit"), {
            "wake_up_time": "06:30", "sleep_time": "22:30", "preferred_study_hours": 3,
            "preferred_study_time": "morning", "daily_available_hours": 5, "academic_goal": "Pass semester one",
        })
        self.assertRedirects(response, reverse("dashboard:home"))
        user.preferences.refresh_from_db()
        self.assertEqual(user.preferences.preferred_study_hours, 3)
