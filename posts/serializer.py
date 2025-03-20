from rest_framework import serializers

from posts.models import Post, Comment
from user.serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'image', 'description']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Title is required')
        if len(value) < 3:
            raise serializers.ValidationError('Title must be at least 3 characters')
        return value

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
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

        if not request.user.is_authenticated():
            raise serializers.ValidationError('You are not authenticated')

        validated_data['post'] = post
        return super().create(validated_data)
