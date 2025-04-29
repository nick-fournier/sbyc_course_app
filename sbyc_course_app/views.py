import json

import gpxpy
import gpxpy.gpx
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .flags import html_flag_tables
from .mapping import COURSE_DATA


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
    