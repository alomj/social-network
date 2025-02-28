from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView

from posts.models import Post
from posts.serializer import PostSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'posts/new_post.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        files = request.FILES

        serializer = PostSerializer(data={**data, **files})
        if serializer.is_valid():
            serializer.save()
            return redirect('list_post')

        return render(request, self.template_name, {'serializer': serializer})