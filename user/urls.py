from django.urls import path

from user.views import RegisterUserAPI, CustomTokenObtainPairView, ResetPasswordTokenRequest, ResetPasswordConfirm

urlpatterns = [
    path('register/', RegisterUserAPI.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('reset-password/', ResetPasswordTokenRequest.as_view(), name='reset_password'),
    path('reset-password/confirm/', ResetPasswordConfirm.as_view(), name='reset_password_confirm'),
]