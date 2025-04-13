from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
import logging
from user.serializer import UserRegistrationSerializer, MyTokenObtainPairSerializer, ResetPasswordRequestSerializer
from .service import ResetPasswordService
logger = logging.getLogger(__name__)
from .tasks import send_email



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        logger.info(response.data, 'Loging request received')
        try:
            if response.status_code == 200:
                token = response.data
                access_token = token['access']
                refresh_token = token['refresh']
                res = Response({'token': access_token, 'refresh_token': refresh_token})
                res.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict'
                )
                res.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict'
                )
                return res
        except (InvalidToken, TokenError) as e:
            logger.error(f"Token error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'error': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterUserAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordTokenRequest(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email address not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = ResetPasswordService.change_password_request(email)

            send_email.delay(
                subject='Reset password request',
                message=f'Reset password request for {email}',
                recipient_list=[email]
                )

            return Response({'token': token})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirm(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            return ResetPasswordService.change_password_confirm(request)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
