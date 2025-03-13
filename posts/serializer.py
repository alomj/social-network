from rest_framework import serializers

from posts.models import Post


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
        return Post.objects.create(**validated_data)
