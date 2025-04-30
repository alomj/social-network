from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from user.models import User
from .post import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like', related_name='liked_comments')

    def __str__(self):
        return f"{self.author}: {self.id}, {self.comment}, {self.post_id}"
