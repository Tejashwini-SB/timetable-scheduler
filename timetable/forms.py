from django import forms
from .models import TimeSlot, Timetable, TimetableEntry, SubjectFacultyAssignment
from departments.models import Section, AcademicYear
from faculty.models import Faculty
from subjects.models import Subject
from classrooms.models import Classroom


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ('day', 'period_number', 'start_time', 'end_time', 'is_break')
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'period_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_break': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ('section', 'academic_year', 'is_active', 'notes')
        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ('time_slot', 'subject', 'faculty', 'classroom', 'is_free', 'notes')
        widgets = {
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional notes'}),
        }

    def __init__(self, *args, **kwargs):
        timetable = kwargs.pop('timetable', None)
        super().__init__(*args, **kwargs)
        if timetable:
            used_slots = timetable.entries.values_list('time_slot_id', flat=True)
            if self.instance.pk:
                used_slots = used_slots.exclude(id=self.instance.time_slot_id)
            self.fields['time_slot'].queryset = TimeSlot.objects.exclude(id__in=used_slots)
            # Filter subjects by section's department
            dept = timetable.section.department
            self.fields['subject'].queryset = Subject.objects.filter(department=dept, is_active=True)


class SubjectFacultyAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubjectFacultyAssignment
        fields = ('subject', 'faculty', 'section', 'academic_year')
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
        }


class TimetableFilterForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='All Departments',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        required=False,
        empty_label='All Academic Years',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=False,
        empty_label='All Sections',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from departments.models import Department
        self.fields['department'].queryset = Department.objects.all()


class AutoScheduleForm(forms.Form):
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    overwrite_existing = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Overwrite existing timetable entries if timetable already exists"
    )
