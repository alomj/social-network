from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.services.profile_service import ProfileDeleter, ProfileGetter, ProfileCreator, ProfileUpdater


class GetProfile(APIView):
    @staticmethod
    def get(request, slug=None):
        serializer = ProfileGetter.get_profile(request=request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateProfile(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def post(request):
        serializer = ProfileCreator.create_profile(user=request.user, data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EditProfile(APIView):
    @staticmethod
    def patch(request, slug=None):
        serializer = ProfileUpdater.update_profile(request=request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProfile(APIView):
    @staticmethod
    def delete(request, slug=None):
        serializer = ProfileDeleter.delete_profile(request=request)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
