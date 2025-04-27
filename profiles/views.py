from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles.services.profile_service import ProfileService

class GetProfile(APIView):
    @staticmethod
    def get(request, slug = None):
        serializer = ProfileService.get_profile(request=request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateProfile(APIView):
    @staticmethod
    def post(request):
        serializer = ProfileService.create_profile(user=request.user, data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EditProfile(APIView):
    @staticmethod
    def patch(request, slug = None, ):
        serializer = ProfileService.update_profile(data=request.data, user=request.user, request=request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProfile(APIView):
    @staticmethod
    def delete(request, slug = None):
        serializer = ProfileService.delete_profile(data=request.data, user=request.user, request=request)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
