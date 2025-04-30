from rest_framework import serializers

from posts.models.post import Post
from posts.serializer import PostSerializer
from profiles.models.profile import Profile
from user.serializer import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['slug', 'avatar', 'user', 'bio', 'followers', 'following', 'posts']
        read_only_fields = ['slug', 'avatar', 'user', 'followers', 'following', 'posts']

    def get_posts(self, obj):
        posts = Post.objects.filter(author=obj.user)
        return PostSerializer(posts, many=True, context=self.context).data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        user = instance.user
        if user_data:
            for key, value in user_data.items():
                setattr(user, key, value)
                user.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class CreateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'user']

    def create(self, validated_data):
        user = self.context['user']
        profile = Profile.objects.create(user=user)
        profile.save()
        return profile
