from django.db import models

from posts.models import Post
from user.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from profiles.manager import ProfileManager
import os

DEFAULT_AVATAR_URL = os.getenv('DEFAULT_AVATAR_URL')


class Profile(models.Model):
    slug = models.SlugField(max_length=100, unique=True, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = CloudinaryField('image', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True, related_query_name='follower')
    following = models.ManyToManyField(User, related_name='following', blank=True, related_query_name='follow')
    posts = models.ManyToManyField(Post, related_name='posts', blank=True, related_query_name='post')

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username} Profile '

    def save(self, *args, **kwargs):
        if not self.avatar or self.avatar == "":
            self.avatar = DEFAULT_AVATAR_URL
        if not self.slug:
            self.slug = slugify(f'{self.user.username}')
        super().save(*args, **kwargs)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return DEFAULT_AVATAR_URL
