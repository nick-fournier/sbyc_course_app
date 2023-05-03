from django.urls import path

from . import views
from . import forms

urlpatterns = [
    path('<int:course_number>-<str:pin>-<str:rounding>/', views.ChartView.as_view(), name='chart-view'),
    path('', views.ChartView.as_view(), name='chart-view-index'),
    # path('<int:course_number>-<str:pin>-<str:rounding>/<str:filepath>/', views.download_gpx)
    path('<int:course_number>-<str:pin>-<str:rounding>/gpx/download', views.gpx_download, name='download'),
    path('<int:course_number>-<str:pin>-<str:rounding>/gpx', views.gpx_string, name='gpx_raw')
]
