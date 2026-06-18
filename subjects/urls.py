from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject_list'),
    path('add/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
]
