from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # Time Slots
    path('timeslots/', views.TimeSlotListView.as_view(), name='timeslot_list'),
    path('timeslots/add/', views.TimeSlotCreateView.as_view(), name='timeslot_create'),
    path('timeslots/<int:pk>/edit/', views.TimeSlotUpdateView.as_view(), name='timeslot_update'),
    path('timeslots/<int:pk>/delete/', views.TimeSlotDeleteView.as_view(), name='timeslot_delete'),

    # Timetables
    path('', views.TimetableListView.as_view(), name='timetable_list'),
    path('create/', views.TimetableCreateView.as_view(), name='timetable_create'),
    path('<int:pk>/', views.TimetableDetailView.as_view(), name='timetable_detail'),
    path('<int:pk>/edit/', views.TimetableUpdateView.as_view(), name='timetable_update'),
    path('<int:pk>/delete/', views.TimetableDeleteView.as_view(), name='timetable_delete'),

    # Entries
    path('<int:timetable_pk>/entries/add/', views.entry_create, name='entry_create'),
    path('entries/<int:pk>/edit/', views.entry_update, name='entry_update'),
    path('entries/<int:pk>/delete/', views.entry_delete, name='entry_delete'),

    # Auto-scheduler
    path('auto-schedule/', views.auto_schedule, name='auto_schedule'),

    # Assignments
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/add/', views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
]
