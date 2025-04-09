from django.urls import path
from .views import PostList, PostCreate, EditPost, DeletePost, CommentPost, ToggleLike
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
                  path('post/', PostList.as_view(), name='list_post'),
                  path('post/create/', PostCreate.as_view(), name='create_post'),
                  path('post/<int:post_id>/edit', EditPost.as_view(), name='edit_post'),
                  path('post/<int:post_id>/delete/', DeletePost.as_view(), name='delete_post'),
                  path('post/<int:post_id>/comment/', CommentPost.as_view(), name='comment_post'),
                  path('post/<int:post_id>/like/', ToggleLike.as_view(), name='like_post'),
                  path('post/comment/like/<int:post_id>/', ToggleLike.as_view(), name='like_comment'),
              ] + debug_toolbar_urls()
