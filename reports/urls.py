from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('timetable/<int:pk>/pdf/', views.timetable_pdf, name='timetable_pdf'),
    path('timetable/<int:pk>/excel/', views.timetable_excel, name='timetable_excel'),
    path('faculty/<int:pk>/pdf/', views.faculty_timetable_pdf, name='faculty_pdf'),
    path('classrooms/', views.classroom_utilization, name='classroom_utilization'),
    path('departments/', views.department_report, name='department_report'),
]
