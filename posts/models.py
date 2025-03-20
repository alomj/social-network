from django.db import models
from cloudinary.models import CloudinaryField

from user.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.title}: {self.created} - {self.description}"

    def get_likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.comment}, {self.post_id}"

    def get_comments_count(self):
        return self.comment.count()


