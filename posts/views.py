from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post
from posts.serializer import PostSerializer, CommentSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny, BasePermission
from .service import PostService


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class PostList(ListAPIView):
    queryset = Post.objects.all()
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
        print(request.FILES)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('list_post')
        print(serializer.errors)
        return render(request, self.template_name, {'serializer': serializer})


class EditPost(APIView):
    permission_classes = [AllowAny]
    template_name = 'posts/edit_post.html'

    @staticmethod
    def get_object(post_id) -> Post:
        return get_object_or_404(Post, id=post_id)

    @staticmethod
    def update(request, post, partial=None) -> Response | HttpResponseRedirect:
        serializer = PostService.update_post(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return Response(serializer.data, status=status.HTTP_200_OK)
            return redirect('list_post')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        post = self.get_object(kwargs['post_id'])
        serializer = PostSerializer(post)
        return render(request, self.template_name, {'serializer': serializer, 'post': post})

    def post(self, request, *args, **kwargs):
        post = self.get_object(kwargs['post_id'])
        return self.update(request, post, partial=True)

    def put(self, request, *args, **kwargs) -> Response | HttpResponseRedirect:
        post = self.get_object(kwargs['post_id'])
        return self.update(request, post, partial=False)

    def patch(self, request, *args, **kwargs) -> Response | HttpResponseRedirect:
        post = self.get_object(kwargs['post_id'])
        return self.update(request, post, partial=True)


class DeletePost(APIView):
    permission_classes = [AllowAny]

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def post(self, request, *args, **kwargs):
        post = self.get_post()
        post.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
        return redirect('list_post')


class LikePost(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        user = self.request.user
        updated = False
        liked = False
        if post.likes.filter(id=user.id).exists():
            liked = False
            post.likes.remove(user)
            updated = True
        else:
            liked = True
            post.likes.add(user)
        data = {
            'liked': liked,
            'updated': updated,
            'likes_count': post.likes.count(),
        }
        return Response(data, status=status.HTTP_200_OK)

class CommentPost(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        author = self.request.user
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)