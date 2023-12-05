from django.urls import path

from . import views
from . import forms

urlpatterns = [
    path('gpx/<int:course_number>-<str:pin>-<str:rounding>/download', views.gpx_download, name='download'),
    path('gpx/<int:course_number>-<str:pin>-<str:rounding>', views.gpx_string, name='gpx_raw'),
    path('chart-app/', views.chart_app, name='chart-app'),
    path('flags/', views.flag_table, name='flag-table'),
    path('', views.index, name='index'),    
]
