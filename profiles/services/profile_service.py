from profiles.serializer import CreateProfileSerializer, ProfileSerializer
from profiles.models import Profile
from rest_framework.exceptions import NotFound


class ProfileGetter:
    @staticmethod
    def get_profile(slug):
        try:
            profile = Profile.objects.get_profile_by_user_slug(slug)
            return profile
        except Profile.DoesNotExist:
            raise NotFound(detail='Profile not found', code='404')


class ProfileCreator:
    @staticmethod
    def create_profile(data, user):
        serializer = CreateProfileSerializer(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return ProfileSerializer(profile)


class ProfileUpdater:
    @staticmethod
    def update_profile(profile, data):
        serializer = ProfileSerializer(data=data, instance=profile, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return ProfileSerializer(profile)


class ProfileDeleter:
    @staticmethod
    def delete_profile(request):
        try:
            profile = Profile.objects.get_profile_by_user_slug(request.user)
            profile.delete()
        except Profile.DoesNotExist:
            raise NotFound(detail='Profile not found', code='404')
