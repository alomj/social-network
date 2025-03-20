from posts.models import Post
from posts.serializer import PostSerializer


class PostService:
    @staticmethod
    def create_post(data):
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer
        return serializer

    @staticmethod
    def update_post(post, data, partial=False):
        serializer = PostSerializer(instance=post, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return serializer
        return serializer

    @staticmethod
    def delete_post(post):
        post.delete()
        return {"message": "Post deleted"}

    @staticmethod
    def like_post(post, user):
        liked = False
        if post.likes.filter(id=user.id).exists():
            liked = False
            post.likes.remove(user)
            updated = True
        else:
            liked = True
            post.likes.add(user)
        return {
            'liked': liked,
            'updated': updated,
            'likes_count': post.likes.count(),
        }
