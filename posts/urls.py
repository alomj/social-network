from django.urls import path
from .views import PostList, PostCreate

urlpatterns = [
    path('post/', PostList.as_view(), name='list_post'),
    path('post/create/', PostCreate.as_view(), name='create_post'),
]