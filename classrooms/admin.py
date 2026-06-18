from django.contrib import admin
from .models import Classroom


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'name', 'building', 'capacity', 'room_type', 'is_available')
    list_filter = ('room_type', 'building', 'is_available', 'has_projector', 'has_ac')
    search_fields = ('room_number', 'name', 'building')
