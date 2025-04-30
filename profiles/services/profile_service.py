from profiles.serializer import CreateProfileSerializer, ProfileSerializer
from profiles.models import Profile
from rest_framework.exceptions import NotFound


class ProfileGetter:
    @staticmethod
    def get_profile(request):
        try:
            return Profile.objects.get_profile_by_user_request(request.user)
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
    def update_profile(request):
        profile = Profile.objects.get_profile_by_user_request(request.user)
        serializer = ProfileSerializer(data=request.data, instance=profile, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return ProfileSerializer(profile)


class ProfileDeleter:
    @staticmethod
    def delete_profile(request):
        try:
            profile = Profile.objects.get_profile_by_user_request(request.user)
            profile.delete()
        except Profile.DoesNotExist:
            raise NotFound(detail='Profile not found', code='404')
