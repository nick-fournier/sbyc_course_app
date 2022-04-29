from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, FormMixin
from .mapping import CourseData
from .forms import CourseForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class ChartView(FormView):
    template_name = 'chart.html'
    form_class = CourseForm

    # Gets the cleaned data to pass
    def form_valid(self, form):
        self.kwargs = form.cleaned_data
        return super().form_valid(form)

    # Receives the cleaned data and updates the success URL accordingly
    def get_success_url(self):
        return '/charts/' + str(self.kwargs['course_number'])

    # Map is then generated based on the URL key
    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        if 'course_number' in self.kwargs:
            course_number = self.kwargs['course_number']
            course_data = CourseData(course_number=course_number)
            chart = course_data.plot_course()._repr_html_()
            context.update({'chart': chart, 'course_number': course_number})
        return context

