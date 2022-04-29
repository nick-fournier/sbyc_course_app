import pandas as pd
from django.views.generic.edit import FormView
from .mapping import CourseCharting
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
        table_classes = 'table table-striped table-bordered table-hover table-sm'

        if 'course_number' in self.kwargs:
            self.kwargs['is_mobile'] = self.request.user_agent.is_mobile
            course = CourseCharting(**self.kwargs)
            course_data = course.plot_course()

            # Render the chart to html and table to json
            course_data['chart'] = course_data['chart']._repr_html_()
            course_data['chart_table'] = course_data['chart_table'].to_html(classes=table_classes, index=False)

            context.update(course_data)

        return context

