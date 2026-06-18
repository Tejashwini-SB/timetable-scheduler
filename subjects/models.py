from django.db import models
from departments.models import Department


class Subject(models.Model):
    SUBJECT_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('lab', 'Laboratory'),
        ('tutorial', 'Tutorial'),
        ('elective', 'Elective'),
    ]

    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE_CHOICES, default='theory')
    credits = models.PositiveIntegerField(default=3)
    hours_per_week = models.PositiveIntegerField(default=3, help_text="Number of periods per week")
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department', 'semester', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f"{self.code} - {self.name}"
