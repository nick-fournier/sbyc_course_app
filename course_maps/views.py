from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .mapping import CourseData

# Create your views here.
class ChartView(TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        course_data = CourseData(course_number=11)
        chart = course_data.plot_course()
        return {"map": chart}

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")