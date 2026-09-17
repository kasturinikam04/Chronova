from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = "Open and verify the configured default database connection."

    def handle(self, *args, **options):
        connection = connections["default"]
        try:
            connection.ensure_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception as exc:
            raise CommandError(f"Database connection failed: {exc}") from exc
        self.stdout.write(self.style.SUCCESS(f"Database connection succeeded ({connection.vendor})."))
