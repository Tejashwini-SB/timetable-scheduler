from django.db import models


class Classroom(models.Model):
    ROOM_TYPE_CHOICES = [
        ('lecture_hall', 'Lecture Hall'),
        ('lab', 'Laboratory'),
        ('seminar_room', 'Seminar Room'),
        ('conference_room', 'Conference Room'),
        ('smart_classroom', 'Smart Classroom'),
    ]

    name = models.CharField(max_length=50)
    room_number = models.CharField(max_length=20, unique=True)
    building = models.CharField(max_length=100, default='Main Building')
    floor = models.CharField(max_length=20, default='Ground Floor')
    capacity = models.PositiveIntegerField(default=60)
    room_type = models.CharField(max_length=30, choices=ROOM_TYPE_CHOICES, default='lecture_hall')
    has_projector = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['building', 'room_number']
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'

    def __str__(self):
        return f"{self.room_number} - {self.name} (Capacity: {self.capacity})"
