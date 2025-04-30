from posts.serializer import CommentSerializer


class CommentService:

    @staticmethod
    def create_comment(data, context):
        serializer = CommentSerializer(data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            return serializer
        return serializer
