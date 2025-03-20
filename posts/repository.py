from django.shortcuts import get_object_or_404
from posts.models import Post

class PostsRepository:
    @staticmethod
    def get_post_by_id(post_id):
        return get_object_or_404(Post, id=post_id)

    @staticmethod
    def get_posts():
        return Post.objects.all()
