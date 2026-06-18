from django import forms
from .models import Faculty
from django.contrib.auth import get_user_model

User = get_user_model()


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = (
            'user', 'department', 'employee_id', 'designation',
            'specialization', 'qualification', 'experience_years',
            'max_hours_per_week', 'joined_date', 'is_active'
        )
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. EMP001'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Machine Learning'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. M.Tech, Ph.D'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'max_hours_per_week': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 40}),
            'joined_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users who don't already have a faculty profile (for create)
        if not self.instance.pk:
            existing_faculty_user_ids = Faculty.objects.values_list('user_id', flat=True)
            self.fields['user'].queryset = User.objects.filter(
                role='faculty'
            ).exclude(id__in=existing_faculty_user_ids)
        else:
            self.fields['user'].queryset = User.objects.filter(role='faculty')
