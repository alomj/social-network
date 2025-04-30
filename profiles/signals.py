from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from profiles.models.profile import Profile
from user.models import User

@receiver([post_save, post_delete], sender=Profile)
def remove_cache(sender, instance, **kwargs):
    cache_key = f'profile-cache-{instance.slug}'
    cache.delete(cache_key)


@receiver([post_save], sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver([post_save], sender=User)
def update_user_info(sender, instance, **kwargs):
    instance.profile.save()