from django.db import models

class ProfileManager(models.Manager):
    def get_profile_by_user_slug(self, slug):
        return self.get(slug=slug)

