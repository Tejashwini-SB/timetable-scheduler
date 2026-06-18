from django.contrib import admin
from .models import TimeSlot, Timetable, TimetableEntry, SubjectFacultyAssignment


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'period_number', 'start_time', 'end_time', 'is_break')
    list_filter = ('day', 'is_break')
    ordering = ('day', 'period_number')


class TimetableEntryInline(admin.TabularInline):
    model = TimetableEntry
    extra = 0
    raw_id_fields = ('time_slot', 'subject', 'faculty', 'classroom')


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('section', 'academic_year', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'academic_year', 'section__department')
    inlines = [TimetableEntryInline]
    search_fields = ('section__name', 'section__department__name')


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ('timetable', 'time_slot', 'subject', 'faculty', 'classroom', 'is_free')
    list_filter = ('time_slot__day', 'is_free', 'timetable__academic_year')
    raw_id_fields = ('timetable', 'time_slot', 'subject', 'faculty', 'classroom')


@admin.register(SubjectFacultyAssignment)
class SubjectFacultyAssignmentAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'subject', 'section', 'academic_year', 'assigned_at')
    list_filter = ('academic_year', 'section__department')
