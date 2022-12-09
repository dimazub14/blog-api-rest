from rest_framework import serializers
from django.contrib.auth.models import User
from apps.blogs.models import Comment, Author, Blog, CustomUser, Tag


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]


class BlogCommentTagSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    author = AuthorSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = "__all__" # Remove field body







