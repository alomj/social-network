from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from cloudinary.models import CloudinaryField
import os

DEFAULT_AVATAR_URL = os.getenv('DEFAULT_AVATAR_URL')


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    avatar = CloudinaryField('image', blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

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
