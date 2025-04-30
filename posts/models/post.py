from django.contrib.contenttypes.fields import  GenericRelation
from django.db import models
from cloudinary.models import CloudinaryField

from user.models import User
from posts.manager import PostsManager


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like', related_name='liked_posts')

    objects = PostsManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.title}: {self.created} - {self.description}"



