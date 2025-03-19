from rest_framework import serializers

from posts.models import Post, Comment
from user.serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

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
        fields = '__all__'

    def validate_comment(self, value):
        if not value:
            raise serializers.ValidationError('Title is required')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
