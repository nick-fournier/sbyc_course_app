from django.urls import path

from . import views
from . import forms

urlpatterns = [
    path('<int:course_number>/', views.ChartView.as_view()),
    path('', views.ChartView.as_view()),
]
