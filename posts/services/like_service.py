from posts.models import Like
from user.serializer import UserSerializer


class LikeService:
    @staticmethod
    def toggle_like(data):
        obj = data['obj']
        content_type = data['content_type']
        author = data['author']

        like, created = Like.objects.get_or_create(
            content_type=content_type,
            object_id=obj.id,
            author=author
        )

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return {'liked': liked, 'author': UserSerializer(author).data}
