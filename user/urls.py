from django.urls import path

from user.views import RegisterAPI, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]