from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='headed_departments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} ({self.code})"


class AcademicYear(models.Model):
    year_label = models.CharField(max_length=20, unique=True, help_text="e.g. 2024-2025")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'

    def __str__(self):
        return self.year_label

    def save(self, *args, **kwargs):
        # Ensure only one current academic year
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Section(models.Model):
    SECTION_CHOICES = [
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
        ('D', 'Section D'),
        ('E', 'Section E'),
    ]

    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]

    name = models.CharField(max_length=5, choices=SECTION_CHOICES, default='A')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sections')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='sections')
    year_of_study = models.IntegerField(choices=YEAR_CHOICES, default=1)
    max_students = models.PositiveIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'department', 'academic_year', 'year_of_study')
        ordering = ['department', 'year_of_study', 'name']
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return f"{self.department.code} - Year {self.year_of_study} - Sec {self.name} ({self.academic_year})"
