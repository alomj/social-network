from rest_framework import status

from profiles.serializer import CreateProfileSerializer, ProfileSerializer
from profiles.models import Profile
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class ProfileGetter:
    @staticmethod
    def get_profile(request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
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
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(data=request.data, instance=profile, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return ProfileSerializer(profile)


class ProfileDeleter:
    @staticmethod
    def delete_profile(request):
        try:
            profile = Profile.objects.get(user=request.user)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            raise NotFound(detail='Profile not found', code='404')
