from django.urls import path
from . import views

app_name = 'classrooms'

urlpatterns = [
    path('', views.ClassroomListView.as_view(), name='classroom_list'),
    path('add/', views.ClassroomCreateView.as_view(), name='classroom_create'),
    path('<int:pk>/edit/', views.ClassroomUpdateView.as_view(), name='classroom_update'),
    path('<int:pk>/delete/', views.ClassroomDeleteView.as_view(), name='classroom_delete'),
]
