from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from .models import Blog, Author, CustomUser
from rest_framework.generics import get_object_or_404
from apps.blogs.models import Comment, Tag
from rest_framework import generics, status, permissions
from apps.blogs.serializers import BlogCommentTagSerializer
from django.db.models import Prefetch, Count
from apps.blogs.filters import BlogFilter
from rest_framework.pagination import PageNumberPagination


class BlogsListAPIViewPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 10000


class BlogsListAPIView(generics.ListAPIView):
    queryset = Blog.objects.prefetch_related("comments", "tags").select_related("author")
    serializer_class = BlogCommentTagSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    # pagination_class = BlogsListAPIViewPagination
    filterset_class = BlogFilter


    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
