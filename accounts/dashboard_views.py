from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()


@login_required
def dashboard_index(request):
    from faculty.models import Faculty
    from subjects.models import Subject
    from classrooms.models import Classroom
    from departments.models import Department, Section, AcademicYear
    from timetable.models import Timetable, TimetableEntry, TimeSlot

    context = {
        'total_faculty': Faculty.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_classrooms': Classroom.objects.count(),
        'total_departments': Department.objects.count(),
        'total_sections': Section.objects.count(),
        'total_timetables': Timetable.objects.filter(is_active=True).count(),
        'total_users': User.objects.count(),
        'total_timeslots': TimeSlot.objects.count(),
        'recent_timetables': Timetable.objects.select_related(
            'section', 'academic_year'
        ).order_by('-created_at')[:5],
        'active_academic_year': AcademicYear.objects.filter(is_current=True).first(),
    }
    return render(request, 'dashboard/index.html', context)
