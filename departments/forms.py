from django import forms
from .models import Department, AcademicYear, Section


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'code', 'description', 'head_of_department')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science Engineering'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CSE'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head_of_department': forms.Select(attrs={'class': 'form-select'}),
        }


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ('year_label', 'start_date', 'end_date', 'is_current')
        widgets = {
            'year_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-2025'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'department', 'academic_year', 'year_of_study', 'max_students')
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'year_of_study': forms.Select(attrs={'class': 'form-select'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120}),
        }
