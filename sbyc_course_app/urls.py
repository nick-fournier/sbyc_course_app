from django.urls import path

from . import views
from . import forms

urlpatterns = [
    path('<int:course_number>-<str:pin>-<str:rounding>/', views.ChartView.as_view(), name='chart-view'),
    path('', views.ChartView.as_view()),
]
