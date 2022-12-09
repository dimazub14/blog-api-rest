from rest_framework import generics
from django_filters import rest_framework as filters
from apps.blogs.models import Blog
#Create Filter


class BlogFilter(filters.FilterSet):
    datetime = filters.DateFromToRangeFilter()

    class Meta:
        model = Blog
        fields = ['title', 'tags', 'datetime', 'author__name', 'author__email']
