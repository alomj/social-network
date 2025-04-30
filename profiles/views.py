from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from profiles.permissions import IsOwner
from profiles.serializer import ProfileSerializer
from profiles.services.profile_service import ProfileDeleter, ProfileGetter, ProfileCreator, ProfileUpdater
from django.core.cache import cache


class GetProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        cache_key = f'profile-cache-{slug}'
        data = cache.get(cache_key)
        if not data:
            profile = ProfileGetter.get_profile(slug)
            serializer = ProfileSerializer(profile)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 10)
        return Response(data, status=status.HTTP_200_OK)


class CreateProfile(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = ProfileCreator.create_profile(user=request.user, data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EditProfile(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, slug):
        profile = ProfileGetter.get_profile(slug)
        self.check_object_permissions(request, profile)
        serializer = ProfileUpdater.update_profile(profile, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProfile(APIView):
    @staticmethod
    def delete(request, slug=None):
        serializer = ProfileDeleter.delete_profile(request=request)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
