from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Count


class PostsManager(models.Manager):
    def get_post_by_id(self, post_id):
        return get_object_or_404(self.model, id=post_id)

    def all_posts(self):
        return self.all()
