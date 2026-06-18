from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'code', 'department', 'subject_type', 'credits', 'hours_per_week', 'semester', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Structures'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS301'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'subject_type': forms.Select(attrs={'class': 'form-select'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'hours_per_week': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
