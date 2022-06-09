from allauth.account.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Course
from django.db.models import Q

class IndexView(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'latest_course_list'

    def get_queryset(self):
        """
        Return the last five published courses
        """
        return Course.objects.all()

class SearchView(generic.ListView):
    model = Course
    template_name = 'main/search.html'

    def get_queryset(self): # new
        return City.objects.filter(
            Q(name__icontains="Boston") | Q(tags__icontains="NY")
        )


@login_required
def course_detail(request, courseID):
    course = Course.objects.get(id=courseID)
    if course is None:
        return HttpResponse("Course not found")
    else:
        return render(request, 'main/course.html', {'course': course, 'stars': range(course.rating//2), 'rem': course.rating%2 == 1 })




