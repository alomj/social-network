from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from .models import User
from .serializer import ResetPasswordRequestSerializer

from rest_framework.response import Response


class ResetPasswordService:
    @staticmethod
    def change_password_request(email):
        token_generator = PasswordResetTokenGenerator()
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        token = token_generator.make_token(user)
        return token

    @staticmethod
    def change_password_confirm(request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data.get('email')

        new_password = data['new_password']
        confirm_new_password = data['confirm_new_password']
        if new_password != confirm_new_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        token = data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        token = token.strip()
        user = User.objects.filter(email__iexact=email).first()

        token_generator = PasswordResetTokenGenerator()

        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user.set_password(new_password)
            user.save()
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        return Response({f'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
