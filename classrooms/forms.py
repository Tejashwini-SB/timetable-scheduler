from django import forms
from .models import Classroom


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ('name', 'room_number', 'building', 'floor', 'capacity', 'room_type', 'has_projector', 'has_ac', 'is_available', 'notes')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Main Lecture Hall'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A101'}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Block A'}),
            'floor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ground Floor'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'has_projector': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_ac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
