from django.urls import path

from . import views

urlpatterns = [
    path('<int:course_number>/', views.ChartView.as_view()),
]
