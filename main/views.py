from django.utils import timezone
from django.shortcuts import render
from django.views import generic

from .models import Course


class IndexView(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'latest_course_list'

    def get_queryset(self):
        """
        Return the last five published courses
        """
        return Course.objects.all()


class DetailView(generic.DetailView):
    model = Course
    template_name = 'main/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Course.objects.first()
