from rest_framework import serializers

from posts.models.post import Post
from posts.models.comment import Comment
from user.serializer import UserSerializer
from django.contrib.contenttypes.models import ContentType


class ToggleLikeSerializer(serializers.Serializer):
    CONTENT_TYPE_MAP = ['Post', 'Comment']

    content_type = serializers.CharField()
    object_id = serializers.IntegerField()

    def validate_content_type(self, value):
        if value not in self.CONTENT_TYPE_MAP:
            raise serializers.ValidationError(f'Content type must be one of {", ".join(self.CONTENT_TYPE_MAP)}')
        return value

    def validate(self, data):
        try:
            content_type = ContentType.objects.get(model=data['content_type'].lower())
            model_class = content_type.model_class()
            obj = model_class.objects.get(id=data['object_id'])
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({'content_type': 'Invalid content type'})
        except model_class.DoesNotExist:
            raise serializers.ValidationError({'object_id': 'Object with this ID does not exist'})

        data['content_type'] = content_type
        data['obj'] = obj
        data['author'] = self.context['request'].user

        return data


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'image', 'description', 'author']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Title is required')
        if len(value) < 3:
            raise serializers.ValidationError('Title must be at least 3 characters')
        return value

    def create(self, validated_data):
        author = self.context['request'].user
        post = Post.objects.create(author=author, **validated_data)

        return post


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['comment', 'author']

    def validate_comment(self, value):
        if not value:
            raise serializers.ValidationError('Title is required')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        post = self.context.get('post')
        author = self.context.get('author')

        if not post:
            raise serializers.ValidationError('Post not found')

        if not author:
            raise serializers.ValidationError('Author not found')

        if not request.user.is_authenticated:
            raise serializers.ValidationError('You are not authenticated')

        validated_data['post'] = post
        return super().create(validated_data)
