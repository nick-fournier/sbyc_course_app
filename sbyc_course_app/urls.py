from django.urls import path

from . import views

urlpatterns = [
    path('gpx/<int:course_number>-<str:pin>-<str:rounding>/download', views.gpx_response_download, name='gpx_download'),
    path('gpx/<int:course_number>-<str:pin>-<str:rounding>', views.gpx_response_raw, name='gpx_raw'),
    path('chart-app/', views.chart_app, name='chart-app'),
    path('flags/', views.flag_table, name='flag-table'),
    path('', views.index, name='sbyc_course_app-index'),    
]
