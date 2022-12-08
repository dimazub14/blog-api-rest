from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
  name = models.CharField(max_length=255)
  email = models.EmailField()

  def __str__(self):
      return self.title


class Blog(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey('Author', related_name='blogs', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=120)
    relates_to = models.ForeignKey('self', on_delete=models.CASCADE)


