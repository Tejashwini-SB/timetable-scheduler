from django.db import models
from departments.models import Department, Section, AcademicYear
from faculty.models import Faculty
from subjects.models import Subject
from classrooms.models import Classroom


class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    period_number = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False, help_text="Mark as lunch/recess break")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day', 'period_number']
        unique_together = ('day', 'period_number')
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'

    def __str__(self):
        return f"{self.day} | P{self.period_number} | {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

    @property
    def duration_minutes(self):
        from datetime import datetime, date
        start = datetime.combine(date.today(), self.start_time)
        end = datetime.combine(date.today(), self.end_time)
        return int((end - start).total_seconds() / 60)


class Timetable(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='timetables')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='timetables')
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        related_name='created_timetables'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('section', 'academic_year')
        ordering = ['-created_at']
        verbose_name = 'Timetable'
        verbose_name_plural = 'Timetables'

    def __str__(self):
        return f"Timetable: {self.section} | {self.academic_year}"


class TimetableEntry(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='entries')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='entries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries', null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='timetable_entries', null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetable_entries', null=True, blank=True)
    is_free = models.BooleanField(default=False, help_text="Mark as free period")
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('timetable', 'time_slot')
        ordering = ['time_slot__day', 'time_slot__period_number']
        verbose_name = 'Timetable Entry'
        verbose_name_plural = 'Timetable Entries'

    def __str__(self):
        subject_name = self.subject.name if self.subject else 'Free Period'
        return f"{self.timetable.section} | {self.time_slot} | {subject_name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        errors = {}

        if self.is_free:
            return

        if self.faculty and self.time_slot_id:
            # Check faculty conflict
            conflict_qs = TimetableEntry.objects.filter(
                faculty=self.faculty,
                time_slot=self.time_slot,
                is_free=False,
            ).exclude(pk=self.pk)
            if conflict_qs.exists():
                other = conflict_qs.first()
                errors['faculty'] = (
                    f"Faculty '{self.faculty}' is already assigned to "
                    f"'{other.timetable.section}' during this time slot."
                )

        if self.classroom and self.time_slot_id:
            # Check classroom conflict
            conflict_qs = TimetableEntry.objects.filter(
                classroom=self.classroom,
                time_slot=self.time_slot,
                is_free=False,
            ).exclude(pk=self.pk)
            if conflict_qs.exists():
                other = conflict_qs.first()
                errors['classroom'] = (
                    f"Classroom '{self.classroom}' is already booked for "
                    f"'{other.timetable.section}' during this time slot."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SubjectFacultyAssignment(models.Model):
    """Maps which faculty can teach which subjects."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='subject_assignments')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subject_assignments', null=True, blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='subject_assignments', null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subject', 'faculty', 'section', 'academic_year')
        verbose_name = 'Subject-Faculty Assignment'
        verbose_name_plural = 'Subject-Faculty Assignments'

    def __str__(self):
        return f"{self.faculty} → {self.subject}"
