from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from cloudinary.models import CloudinaryField

from user.models import User
from .manager import PostsManager


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


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like', related_name='liked_comments')

    def __str__(self):
        return f"{self.author}: {self.id}, {self.comment}, {self.post_id}"


class Like(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_type', 'object_id')
        indexes = [models.Index(fields=['content_type', 'object_id'])]
