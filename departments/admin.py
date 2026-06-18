from django.contrib import admin
from .models import Department, AcademicYear, Section


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at',)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year_label', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'academic_year', 'year_of_study', 'max_students')
    list_filter = ('department', 'academic_year', 'year_of_study')
    search_fields = ('name', 'department__name')
