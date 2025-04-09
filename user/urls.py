from django.urls import path

from user.views import RegisterUserAPI, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterUserAPI.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]