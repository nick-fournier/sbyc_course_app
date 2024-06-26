from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
import gpxpy
import gpxpy.gpx

from .mapping import COURSE_DATA
from .flags import html_flag_tables


# Returns the serialized course string as file in GPX format
def gpx_response_download(request,  **kwargs):
    gpx_xml = create_gpx(**kwargs).to_xml()
    course_no = kwargs.get('course_number')
    rounding = kwargs.get('rounding') 
    
    filename = f"sbyc_fns_course_{course_no}_{rounding}.gpx"   

    response = HttpResponse(gpx_xml, content_type='application/gpx')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

# Returns the serialized course string in GPX format
def gpx_response_raw(request, **kwargs):
    gpx_xml = create_gpx(**kwargs).to_xml()
    return HttpResponse(gpx_xml, content_type='application/xml')

def create_gpx(**kwargs):    
    course_no = kwargs.get('course_number', '')
    rounding = kwargs.get('rounding', '').lower()
    course = COURSE_DATA[course_no]

    # Create a gpx object
    gpx = gpxpy.gpx.GPX()

    # Create first route in our GPX
    gpx_route = gpxpy.gpx.GPXRoute()
    gpx.routes.append(gpx_route)
    
    # Populate the route with points
    gpx_route.name = f"SBYC FNS Course #{course_no} {rounding} windward rounding"
    for pt in course:
        gpx_route.points.append(
            gpxpy.gpx.GPXRoutePoint(pt['lat'], pt['lon'])
        )
    
    return gpx


# class ChartView(FormView):
#     template_name = 'chart.html'
#     form_class = CourseForm

#     # Gets the cleaned data to pass
#     def form_valid(self, form):
#         self.form = form
#         return super().form_valid(form)

#     def get_form_kwargs(self):
#         kwargs = super(ChartView, self).get_form_kwargs()
#         url_kwargs = {'url_kwargs': self.kwargs}  # self.kwargs contains all url conf params
#         kwargs.update(url_kwargs)
#         return kwargs

#     # Receives the cleaned data and updates the success URL accordingly
#     def get_success_url(self):
#         # Add default values
#         kwargs = self.form.cleaned_data
#         kwargs['pin'] = kwargs.get('pin', 'RC BOAT')
#         kwargs['rounding'] = kwargs.get('rounding', 'PORT')
        
#         return reverse_lazy('chart-view', kwargs=kwargs)

#     # Map is then generated based on the URL key
#     def get_context_data(self, **kwargs):
#         context = super(ChartView, self).get_context_data(**kwargs)
#         html_table_classes = 'table table-striped table-bordered table-hover table-sm'
#         context.update(html_flag_tables(html_table_classes))

#         if 'course_number' in self.kwargs:
#             # Generate course plot
#             self.kwargs['is_mobile'] = self.request.user_agent.is_mobile # type: ignore
#             course = CourseCharting(**self.kwargs)
#             course_data = course.plot_course()
                        
#             # Add kwargs to context
#             context.update(self.kwargs)    
                        
#             # Render the chart to html and table to json
#             course_data['chart'] = course_data['chart']._repr_html_()
#             course_data['chart_table'] = course_data['chart_table'].to_html(classes=html_table_classes, index=False)
#             context.update(course_data)

#         return context

def chart_app(request, **kwargs):
    
    # Convert dataframe to json
    html_table_classes = 'table table-striped table-bordered table-hover table-sm'
        
    context = kwargs
    context['course_data'] = json.dumps(COURSE_DATA)

    context.update(html_flag_tables(html_table_classes))

    return render(request, 'chart_app.html', context=context)

def flag_table(request):
    html_table_classes = 'table table-striped table-bordered table-hover table-sm'
    context = html_flag_tables(html_table_classes)
    return render(request, 'flag_table.html', context=context)

def index(request):
    return redirect("chart-app")
    