from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    # Departments
    path('', views.DepartmentListView.as_view(), name='department_list'),
    path('add/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Academic Years
    path('academic-years/', views.AcademicYearListView.as_view(), name='academic_year_list'),
    path('academic-years/add/', views.AcademicYearCreateView.as_view(), name='academic_year_create'),
    path('academic-years/<int:pk>/edit/', views.AcademicYearUpdateView.as_view(), name='academic_year_update'),
    path('academic-years/<int:pk>/delete/', views.AcademicYearDeleteView.as_view(), name='academic_year_delete'),

    # Sections
    path('sections/', views.SectionListView.as_view(), name='section_list'),
    path('sections/add/', views.SectionCreateView.as_view(), name='section_create'),
    path('sections/<int:pk>/edit/', views.SectionUpdateView.as_view(), name='section_update'),
    path('sections/<int:pk>/delete/', views.SectionDeleteView.as_view(), name='section_delete'),
]
