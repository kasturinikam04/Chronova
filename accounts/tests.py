from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountFlowTests(TestCase):
    def test_registration_creates_user_profile_and_preferences(self):
        response = self.client.post(reverse("accounts:register"), {
            "full_name": "Sample Student", "username": "sample_student", "email": "sample@example.com",
            "password1": "Strong-pass-2026!", "password2": "Strong-pass-2026!",
        })
        self.assertRedirects(response, reverse("dashboard:home"))
        user = User.objects.get(username="sample_student")
        self.assertEqual(user.profile.full_name, "Sample Student")
        self.assertEqual(user.preferences.daily_available_hours, 2)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user("existing", "taken@example.com", "Strong-pass-2026!")
        response = self.client.post(reverse("accounts:register"), {
            "full_name": "Another Student", "username": "another", "email": "taken@example.com",
            "password1": "Strong-pass-2026!", "password2": "Strong-pass-2026!",
        })
        self.assertContains(response, "already exists")
