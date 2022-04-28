from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from mapping import CourseData

# Create your views here.
class FoliumView(TemplateView):
    template_name = "folium_app/map.html"

    def get_context_data(self, **kwargs):
        map = CourseData.plot_course(11)
        return {"map": map}

