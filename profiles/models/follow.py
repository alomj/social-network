from django.db import models

class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} Following {self.following.username}'