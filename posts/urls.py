from django.urls import path
from .views import PostList, PostCreate, EditPost, DeletePost

urlpatterns = [
    path('post/', PostList.as_view(), name='list_post'),
    path('post/create/', PostCreate.as_view(), name='create_post'),
    path('post/<int:post_id>/edit', EditPost.as_view(), name='edit_post'),
    path('post/<int:post_id>/delete/', DeletePost.as_view(), name='delete_post'),
]