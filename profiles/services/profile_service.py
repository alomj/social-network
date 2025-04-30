from profiles.serializer import CreateProfileSerializer, ProfileSerializer
from profiles.models.profile import Profile
from rest_framework.exceptions import NotFound
from rest_framework import status

class ProfileGetter:
    @staticmethod
    def get_profile(slug):
        try:
            profile = Profile.objects.get_profile_by_user_slug(slug)
            return profile
        except Profile.DoesNotExist:
            raise NotFound(detail='Profile not found', code=status.HTTP_404_NOT_FOUND)


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
            raise NotFound(detail='Profile not found', code=status.HTTP_404_NOT_FOUND)
