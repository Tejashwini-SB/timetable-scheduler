from django.contrib import admin
from .models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'department', 'designation', 'experience_years', 'is_active')
    list_filter = ('department', 'designation', 'is_active')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email')
    raw_id_fields = ('user',)
    ordering = ('employee_id',)
