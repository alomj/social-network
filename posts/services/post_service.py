from posts.models import Post
from posts.serializer import PostSerializer


class PostService:
    @staticmethod
    def create_post(request, data):
        author = request.user
        context = {'request': request, 'author': author}
        serializer = PostSerializer(data=data, context=context)
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

