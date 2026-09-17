from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Preference


@receiver(post_save, sender=User)
def create_preferences(sender, instance, created, **kwargs):
    if created:
        Preference.objects.create(user=instance)
