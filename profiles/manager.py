from django.db import models

class ProfileManager(models.Manager):
    def get_profile_by_user_request(self, user):
        return self.get(user=user)

