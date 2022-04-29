from django.views.generic.edit import FormView
from .mapping import CourseData
from .forms import CourseForm


class ChartView(FormView):
    template_name = 'chart.html'
    form_class = CourseForm

    # Gets the cleaned data to pass
    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ChartView, self).get_form_kwargs()
        url_kwargs = {'url_kwargs': self.kwargs}  # self.kwargs contains all url conf params
        kwargs.update(url_kwargs)
        return kwargs

    # Receives the cleaned data and updates the success URL accordingly
    def get_success_url(self):
        url = '/charts/'
        url += '-'.join([str(x) for x in self.form.cleaned_data.values()])
        return url

    # Map is then generated based on the URL key
    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        if 'course_number' in self.kwargs:
            course_number = self.kwargs['course_number']
            # course_data = CourseData(course_number=course_number)
            course_data = CourseData(**self.kwargs)
            chart = course_data.plot_course()._repr_html_()
            context.update({'chart': chart, 'course_number': course_number})
        return context

