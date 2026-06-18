from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count

from .models import Faculty
from .forms import FacultyForm
from accounts.views import AdminRequiredMixin


class FacultyListView(LoginRequiredMixin, ListView):
    model = Faculty
    template_name = 'faculty/faculty_list.html'
    context_object_name = 'faculty_list'
    paginate_by = 15

    def get_queryset(self):
        qs = Faculty.objects.select_related('user', 'department').order_by('employee_id')
        search = self.request.GET.get('search', '')
        dept = self.request.GET.get('department', '')
        active = self.request.GET.get('active', '')
        if search:
            qs = qs.filter(
                Q(employee_id__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(specialization__icontains=search)
            )
        if dept:
            qs = qs.filter(department_id=dept)
        if active == 'true':
            qs = qs.filter(is_active=True)
        elif active == 'false':
            qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from departments.models import Department
        ctx['departments'] = Department.objects.all()
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_dept'] = self.request.GET.get('department', '')
        ctx['selected_active'] = self.request.GET.get('active', '')
        return ctx


class FacultyDetailView(LoginRequiredMixin, DetailView):
    model = Faculty
    template_name = 'faculty/faculty_detail.html'
    context_object_name = 'faculty'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['assignments'] = self.object.subject_assignments.select_related(
            'subject', 'section', 'academic_year'
        )
        ctx['timetable_entries'] = self.object.timetable_entries.select_related(
            'timetable__section', 'time_slot', 'subject', 'classroom'
        ).order_by('time_slot__day', 'time_slot__period_number')[:50]
        return ctx


class FacultyCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'faculty/faculty_form.html'
    success_url = reverse_lazy('faculty:faculty_list')

    def form_valid(self, form):
        messages.success(self.request, f"Faculty '{form.instance.full_name}' added successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Faculty'
        ctx['action'] = 'Create'
        return ctx


class FacultyUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'faculty/faculty_form.html'
    success_url = reverse_lazy('faculty:faculty_list')

    def form_valid(self, form):
        messages.success(self.request, f"Faculty '{form.instance.full_name}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Faculty'
        ctx['action'] = 'Update'
        return ctx


class FacultyDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Faculty
    template_name = 'faculty/faculty_confirm_delete.html'
    success_url = reverse_lazy('faculty:faculty_list')

    def form_valid(self, form):
        messages.success(self.request, "Faculty record deleted.")
        return super().form_valid(form)
