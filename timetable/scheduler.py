"""
Auto-scheduling engine for the Timetable Scheduler.
Uses a constraint-based greedy algorithm to assign subjects→faculty→classrooms→timeslots.
"""
import random
from collections import defaultdict

from .models import TimeSlot, Timetable, TimetableEntry, SubjectFacultyAssignment
from subjects.models import Subject
from faculty.models import Faculty
from classrooms.models import Classroom
from departments.models import Section, AcademicYear


class SchedulerEngine:
    def __init__(self, section: Section, academic_year: AcademicYear):
        self.section = section
        self.academic_year = academic_year
        self.department = section.department
        self.errors = []
        self.warnings = []

    def get_or_create_timetable(self, overwrite=False):
        timetable, created = Timetable.objects.get_or_create(
            section=self.section,
            academic_year=self.academic_year,
            defaults={'created_by': None}
        )
        if not created and overwrite:
            timetable.entries.all().delete()
        return timetable, created

    def check_conflicts(self, faculty, classroom, time_slot, exclude_entry_id=None):
        """Return list of conflict descriptions."""
        conflicts = []
        faculty_qs = TimetableEntry.objects.filter(
            faculty=faculty, time_slot=time_slot, is_free=False
        )
        if exclude_entry_id:
            faculty_qs = faculty_qs.exclude(pk=exclude_entry_id)
        if faculty_qs.exists():
            conflict = faculty_qs.first()
            conflicts.append(f"Faculty '{faculty}' already assigned at this slot (→ {conflict.timetable.section})")

        classroom_qs = TimetableEntry.objects.filter(
            classroom=classroom, time_slot=time_slot, is_free=False
        )
        if exclude_entry_id:
            classroom_qs = classroom_qs.exclude(pk=exclude_entry_id)
        if classroom_qs.exists():
            conflict = classroom_qs.first()
            conflicts.append(f"Classroom '{classroom}' already booked at this slot (→ {conflict.timetable.section})")

        return conflicts

    def auto_schedule(self, overwrite=False):
        """
        Greedy auto-scheduler:
        1. Loads subjects assigned to this section
        2. Finds matching faculty per subject
        3. Iterates available time slots
        4. Assigns without conflicts
        """
        timetable, created = self.get_or_create_timetable(overwrite)

        # All time slots (non-break)
        time_slots = list(TimeSlot.objects.filter(is_break=False).order_by('day', 'period_number'))
        if not time_slots:
            self.errors.append("No time slots defined. Please add time slots first.")
            return timetable, False

        # Subject assignments for this section
        assignments = SubjectFacultyAssignment.objects.filter(
            section=self.section,
            academic_year=self.academic_year,
        ).select_related('subject', 'faculty')

        if not assignments.exists():
            self.errors.append("No subject-faculty assignments found for this section. Please assign subjects to faculty first.")
            return timetable, False

        # Available classrooms
        classrooms = list(Classroom.objects.filter(is_available=True).order_by('capacity'))
        if not classrooms:
            self.errors.append("No classrooms available. Please add classrooms.")
            return timetable, False

        # Already used slots in this timetable
        used_slots = set(timetable.entries.values_list('time_slot_id', flat=True))

        # Build schedule tasks: each assignment repeated hours_per_week times
        tasks = []
        for assignment in assignments:
            subject = assignment.subject
            faculty = assignment.faculty
            hours = subject.hours_per_week
            for _ in range(hours):
                tasks.append((subject, faculty))

        # Shuffle to distribute evenly across days
        random.shuffle(tasks)

        assigned_count = 0
        for subject, faculty in tasks:
            # Find a suitable slot
            for slot in time_slots:
                if slot.id in used_slots:
                    continue

                # Find a suitable classroom
                suitable_room = None
                for room in classrooms:
                    if room.capacity >= self.section.max_students:
                        conflicts = self.check_conflicts(faculty, room, slot)
                        if not conflicts:
                            suitable_room = room
                            break

                if suitable_room is None:
                    # Try with any room (capacity might be less but no conflicts)
                    for room in classrooms:
                        conflicts = self.check_conflicts(faculty, room, slot)
                        if not conflicts:
                            suitable_room = room
                            self.warnings.append(
                                f"Room {room.room_number} assigned to {subject.name} has capacity "
                                f"{room.capacity} < section size {self.section.max_students}"
                            )
                            break

                if suitable_room is not None:
                    TimetableEntry.objects.create(
                        timetable=timetable,
                        time_slot=slot,
                        subject=subject,
                        faculty=faculty,
                        classroom=suitable_room,
                        is_free=False,
                    )
                    used_slots.add(slot.id)
                    assigned_count += 1
                    break
            else:
                self.warnings.append(
                    f"Could not find a conflict-free slot for '{subject.name}' "
                    f"with faculty '{faculty}'. Please assign manually."
                )

        if assigned_count == 0:
            self.errors.append("Auto-scheduler could not assign any slots. Check faculty assignments and time slots.")
            return timetable, False

        return timetable, True
