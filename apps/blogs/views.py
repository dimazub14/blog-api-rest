from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.generics import get_object_or_404
from apps.blog.models import Comment
from rest_framework import generics
from django.core import serializers as core_serializers
from apps.blog.serializers import BlogSerializer


class BlogView(APIView):

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({"blogs": serializer.data})

    def post(self, request):
        blog = request.data.get('blogs')
        serializer = BlogSerializer(data=blog)
        if serializer.is_valid(raise_exception=True):
            blog_saved = serializer.save()
        return Response({"success": "Blog '{}' created successfully"
                        .format(blog_saved.title)})

    def put(self, request, pk):
        saved_blog = get_object_or_404(Blog.objects.all(), pk=pk)
        data = request.data.get('Blogs')
        serializer = BlogSerializer(instance=saved_blog, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            blog_saved = serializer.save()
        return Response({
            "success": "Article '{}' updated successfully".format(blog_saved.title)
        })

    def delete(self, request, pk):
        # Get object with this pk
        blog = get_object_or_404(Blog.objects.all(), pk=pk)
        blog.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = core_serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = core_serializers.CommentSerializer
