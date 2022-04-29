from django.views.generic import TemplateView, DetailView
from .mapping import CourseData
from django.shortcuts import redirect

class ChartView(TemplateView):
    template_name = "chart.html"

    def get_context_data(self, **kwargs):
        course_number = self.kwargs['course_number']
        course_data = CourseData(course_number=course_number)
        chart = course_data.plot_course()._repr_html_()
        return {'chart': chart, 'course_number': course_number}
