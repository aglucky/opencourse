from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

from taggit.managers import TaggableManager



class Course(models.Model):
    url = models.CharField(max_length=2048)
    description = models.CharField(max_length=5000, default="")
    name = models.CharField(max_length=200, default="")
    number = models.CharField(max_length=200, default="")
    created_date = models.DateTimeField(default=timezone.now)
    college = models.CharField(max_length=200, default="")
    tags = TaggableManager()
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.CharField(max_length=5000)
    rating = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.name}'