from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username


class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    author = models.ForeignKey(Author, related_name='blogs', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=120)
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    relates_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.author} - {self.blog}"

#Add tags to Blog
#1. Blog + Comment + Tag
#2. Blog where tag == tags + Comment + Tag



