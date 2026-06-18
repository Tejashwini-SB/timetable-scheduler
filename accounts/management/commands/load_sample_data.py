"""
Management command to populate the database with sample data for testing.
Run: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, time

User = get_user_model()


class Command(BaseCommand):
    help = 'Load sample data for development and testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))

        # ─── Users ────────────────────────────────────────────────────────────
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@edu.in',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        faculty_users_data = [
            ('dr.sharma', 'Rajesh', 'Sharma', 'rssharma@edu.in'),
            ('dr.patel', 'Meera', 'Patel', 'mpatel@edu.in'),
            ('dr.kumar', 'Anil', 'Kumar', 'akumar@edu.in'),
            ('prof.singhania', 'Priya', 'Singhania', 'psinghania@edu.in'),
        ]
        faculty_user_objs = []
        for uname, first, last, email in faculty_users_data:
            u, _ = User.objects.get_or_create(username=uname, defaults={
                'email': email, 'first_name': first, 'last_name': last, 'role': 'faculty'
            })
            u.set_password('faculty123')
            u.save()
            faculty_user_objs.append(u)

        self.stdout.write('  ✓ Users created')

        # ─── Departments ──────────────────────────────────────────────────────
        from departments.models import Department, AcademicYear, Section
        dept_cse, _ = Department.objects.get_or_create(
            code='CSE', defaults={'name': 'Computer Science Engineering', 'description': 'Dept of CS'}
        )
        dept_ece, _ = Department.objects.get_or_create(
            code='ECE', defaults={'name': 'Electronics & Communication Engineering', 'description': 'Dept of ECE'}
        )
        self.stdout.write('  ✓ Departments created')

        # ─── Academic Year ────────────────────────────────────────────────────
        ay, _ = AcademicYear.objects.get_or_create(
            year_label='2024-2025',
            defaults={'start_date': date(2024, 8, 1), 'end_date': date(2025, 5, 31), 'is_current': True}
        )
        self.stdout.write('  ✓ Academic year created')

        # ─── Sections ─────────────────────────────────────────────────────────
        sec_a, _ = Section.objects.get_or_create(
            name='A', department=dept_cse, academic_year=ay, year_of_study=3,
            defaults={'max_students': 60}
        )
        sec_b, _ = Section.objects.get_or_create(
            name='B', department=dept_cse, academic_year=ay, year_of_study=3,
            defaults={'max_students': 60}
        )
        self.stdout.write('  ✓ Sections created')

        # ─── Faculty ──────────────────────────────────────────────────────────
        from faculty.models import Faculty
        faculty_objs = []
        faculty_specs = [
            ('EMP001', 'professor', 'Machine Learning', 'Ph.D Computer Science', 15),
            ('EMP002', 'associate_professor', 'VLSI Design', 'M.Tech ECE', 10),
            ('EMP003', 'assistant_professor', 'Data Structures', 'M.Tech CS', 5),
            ('EMP004', 'assistant_professor', 'Computer Networks', 'M.Tech CS', 7),
        ]
        for i, (emp_id, designation, spec, qual, exp) in enumerate(faculty_specs):
            f, _ = Faculty.objects.get_or_create(
                employee_id=emp_id,
                defaults={
                    'user': faculty_user_objs[i],
                    'department': dept_cse,
                    'designation': designation,
                    'specialization': spec,
                    'qualification': qual,
                    'experience_years': exp,
                    'max_hours_per_week': 18,
                    'is_active': True,
                }
            )
            faculty_objs.append(f)
        self.stdout.write('  ✓ Faculty created')

        # ─── Subjects ─────────────────────────────────────────────────────────
        from subjects.models import Subject
        subjects_data = [
            ('CS301', 'Data Structures & Algorithms', 'theory', 4, 4, 5),
            ('CS302', 'Database Management Systems', 'theory', 3, 3, 5),
            ('CS303', 'Computer Networks', 'theory', 3, 3, 5),
            ('CS304', 'Operating Systems', 'theory', 3, 3, 5),
            ('CS305L', 'DSA Lab', 'lab', 2, 2, 5),
        ]
        subject_objs = []
        for code, name, stype, credits, hrs, sem in subjects_data:
            s, _ = Subject.objects.get_or_create(
                code=code,
                defaults={'name': name, 'department': dept_cse, 'subject_type': stype,
                          'credits': credits, 'hours_per_week': hrs, 'semester': sem, 'is_active': True}
            )
            subject_objs.append(s)
        self.stdout.write('  ✓ Subjects created')

        # ─── Classrooms ───────────────────────────────────────────────────────
        from classrooms.models import Classroom
        rooms_data = [
            ('A101', 'Main Hall', 'Block A', 'Ground Floor', 80, 'lecture_hall'),
            ('A102', 'Room 102', 'Block A', 'Ground Floor', 60, 'lecture_hall'),
            ('B201', 'Seminar Hall', 'Block B', 'Second Floor', 40, 'seminar_room'),
            ('C101', 'CS Lab 1', 'Block C', 'Ground Floor', 40, 'lab'),
        ]
        classroom_objs = []
        for num, name, building, floor, cap, rtype in rooms_data:
            r, _ = Classroom.objects.get_or_create(
                room_number=num,
                defaults={'name': name, 'building': building, 'floor': floor,
                          'capacity': cap, 'room_type': rtype, 'is_available': True, 'has_projector': True}
            )
            classroom_objs.append(r)
        self.stdout.write('  ✓ Classrooms created')

        # ─── Time Slots ───────────────────────────────────────────────────────
        from timetable.models import TimeSlot
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = [
            (1, time(9, 0), time(10, 0)),
            (2, time(10, 0), time(11, 0)),
            (3, time(11, 15), time(12, 15)),
            (4, time(12, 15), time(13, 15)),
            (5, time(14, 0), time(15, 0)),
            (6, time(15, 0), time(16, 0)),
        ]
        for day in days:
            for p_num, start, end in periods:
                TimeSlot.objects.get_or_create(
                    day=day, period_number=p_num,
                    defaults={'start_time': start, 'end_time': end, 'is_break': False}
                )
        self.stdout.write('  ✓ Time slots created (5 days × 6 periods)')

        # ─── Subject-Faculty Assignments ──────────────────────────────────────
        from timetable.models import SubjectFacultyAssignment
        assign_data = [
            (subject_objs[0], faculty_objs[0], sec_a),   # DSA → Dr. Sharma
            (subject_objs[1], faculty_objs[2], sec_a),   # DBMS → Dr. Kumar
            (subject_objs[2], faculty_objs[3], sec_a),   # Networks → Prof. Singhania
            (subject_objs[3], faculty_objs[0], sec_a),   # OS → Dr. Sharma
            (subject_objs[4], faculty_objs[2], sec_a),   # DSA Lab → Dr. Kumar
        ]
        for subj, fac, sec in assign_data:
            SubjectFacultyAssignment.objects.get_or_create(
                subject=subj, faculty=fac, section=sec, academic_year=ay
            )
        self.stdout.write('  ✓ Subject-Faculty assignments created')

        self.stdout.write(self.style.SUCCESS(
            '\n✅ Sample data loaded successfully!\n'
            '   Admin login: admin / admin123\n'
            '   Faculty login: dr.sharma / faculty123\n'
            '   Now run: python manage.py runserver\n'
            '   Then go to http://127.0.0.1:8000/timetable/auto-schedule/ to auto-generate!'
        ))
