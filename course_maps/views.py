from django.views.generic import TemplateView
from .mapping import CourseData


class ChartView(TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        course_data = CourseData(course_number=11)
        chart = course_data.plot_course()._repr_html_()
        return {"chart": chart}
