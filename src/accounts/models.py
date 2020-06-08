from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_api_token(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    """
    Creates an API Token just after user creation.
    """
    if created:
        Token.objects.create(user=instance)
