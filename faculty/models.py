from django.db import models
from django.contrib.auth import get_user_model
from departments.models import Department

User = get_user_model()


class Faculty(models.Model):
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('senior_lecturer', 'Senior Lecturer'),
        ('visiting_faculty', 'Visiting Faculty'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='faculty_members')
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES, default='assistant_professor')
    specialization = models.CharField(max_length=200, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    max_hours_per_week = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculty Members'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def email(self):
        return self.user.email
