from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DashboardTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:home')}")

    def test_dashboard_shows_placeholder_cards(self):
        user = User.objects.create_user("sample", "sample@example.com", "Strong-pass-2026!")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard:home"))
        self.assertContains(response, "Attendance")
        self.assertContains(response, "Study hours")
