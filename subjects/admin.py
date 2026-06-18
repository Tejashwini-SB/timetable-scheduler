from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'subject_type', 'credits', 'semester', 'is_active')
    list_filter = ('department', 'subject_type', 'semester', 'is_active')
    search_fields = ('code', 'name')
    ordering = ('department', 'semester', 'name')
