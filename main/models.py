from django.db import models
from django.utils import timezone
from django.contrib import admin


class Tag(models.Model):
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name
        
class Course(models.Model):
    url = models.CharField(max_length=2048)
    description = models.CharField(max_length=5000, default="")
    name = models.CharField(max_length=200, default="")
    number = models.CharField(max_length=200, default="")
    created_date = models.DateTimeField(default=timezone.now)
    college = models.CharField(max_length=200, default="")
    tags = models.ManyToManyField(Tag)


    def __str__(self):
        return self.name



