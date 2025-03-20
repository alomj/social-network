from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post
from posts.serializer import PostSerializer, CommentSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny

from posts.services.comment_service import CommentService
from posts.services.post_service import PostService
from posts.permissions import IsOwnerOrReadOnly, ReadOnly
from posts.repository import PostsRepository


class PostList(ListAPIView):
    permission_classes = [ReadOnly]
    queryset = PostsRepository.get_posts()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'posts/home.html'
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        return render(request, self.template_name, {'posts': posts})


class PostCreate(APIView):
    permission_classes = [AllowAny]
    template_name = 'posts/new_post.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        serializer = PostService.create_post(request.data)
        print(serializer.errors)
        if not serializer.errors:
            return redirect('list_post')
        return render(request, self.template_name, {'serializer': serializer})


class EditPost(APIView):
    permission_classes = [AllowAny]
    template_name = 'posts/edit_post.html'


    def get(self, request, *args, **kwargs):
        post = PostsRepository.get_post_by_id(kwargs['post_id'])
        serializer = PostSerializer(post)
        return render(request, self.template_name, {'serializer': serializer, 'post': post})

    def post(self, request, *args, **kwargs):
        post = PostsRepository.get_post_by_id(kwargs['post_id'])
        serializer = PostService.update_post(post, request.data, partial=True)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response(serializer.data, status=status.HTTP_200_OK)
        if not serializer.errors:
            return redirect('list_post')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeletePost(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



    def post(self, request, *args, **kwargs):
        post = PostsRepository.get_post_by_id(kwargs['post_id'])
        PostService.delete_post(post)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
        return redirect('list_post')


class LikePost(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        result = PostService.like_post(post, request.user)
        return Response(result, status=status.HTTP_200_OK)


class CommentPost(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        post = PostsRepository.get_post_by_id(kwargs['post_id'])
        author = self.request.user
        context = {'request': request, 'post': post, 'author': author}
        serializer, errors = CommentService.create_comment(data=request.data, context=context )
        if not errors:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
