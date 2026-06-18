from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    path('', views.FacultyListView.as_view(), name='faculty_list'),
    path('add/', views.FacultyCreateView.as_view(), name='faculty_create'),
    path('<int:pk>/', views.FacultyDetailView.as_view(), name='faculty_detail'),
    path('<int:pk>/edit/', views.FacultyUpdateView.as_view(), name='faculty_update'),
    path('<int:pk>/delete/', views.FacultyDeleteView.as_view(), name='faculty_delete'),
]
