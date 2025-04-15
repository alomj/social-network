from django.db import models

from user.models import User
from cloudinary.models import CloudinaryField

import os

DEFAULT_AVATAR_URL = os.getenv('DEFAULT_AVATAR_URL')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = CloudinaryField('image', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.avatar or self.avatar =="":
            self.avatar = DEFAULT_AVATAR_URL
        super().save(*args, **kwargs)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return DEFAULT_AVATAR_URL
