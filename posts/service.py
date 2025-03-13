from posts.models import Post
from .serializer import PostSerializer

class PostService:
    @staticmethod
    def update_post(post, data, partial=False):
        serializer = PostSerializer(instance=post, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return serializer
        return serializer