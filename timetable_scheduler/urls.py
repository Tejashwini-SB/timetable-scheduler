"""
URL configuration for timetable_scheduler project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('accounts.dashboard_urls', namespace='dashboard')),
    path('departments/', include('departments.urls', namespace='departments')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('subjects/', include('subjects.urls', namespace='subjects')),
    path('classrooms/', include('classrooms.urls', namespace='classrooms')),
    path('timetable/', include('timetable.urls', namespace='timetable')),
    path('reports/', include('reports.urls', namespace='reports')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
