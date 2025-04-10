from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Count, Sum

class PostsManager(models.Manager):
    def get_post_by_id(self, post_id):
        return get_object_or_404(self.model, id=post_id)

    def all_posts(self):
        return self.all()

    def get_likes_and_comment_counts(self):
        return self.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comment'))

    def get_comments_counts(self):
        return self.annotate(comments=Count('comment')).filter(comments__gt=0).count()
