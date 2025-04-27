from django.urls import path
from profiles.views import GetProfile, CreateProfile, EditProfile, DeleteProfile

urlpatterns = [
    path('create/', CreateProfile.as_view(), name='create-profile'),
    path('<slug:slug>/edit/', EditProfile.as_view(), name='editing-profile'),
    path('<slug:slug>/', GetProfile.as_view(), name='get-profile'),
    path('<slug:slug>/delete/', DeleteProfile.as_view(), name='delete-profile'),

]
