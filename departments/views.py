from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Department, AcademicYear, Section
from .forms import DepartmentForm, AcademicYearForm, SectionForm
from accounts.views import AdminRequiredMixin


# ─── Department CRUD ─────────────────────────────────────────────────────────

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(code__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search'] = self.request.GET.get('search', '')
        return ctx


class DepartmentCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('departments:department_list')

    def form_valid(self, form):
        messages.success(self.request, f"Department '{form.instance.name}' created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Department'
        ctx['action'] = 'Create'
        return ctx


class DepartmentUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('departments:department_list')

    def form_valid(self, form):
        messages.success(self.request, f"Department '{form.instance.name}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Department'
        ctx['action'] = 'Update'
        return ctx


class DepartmentDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('departments:department_list')

    def form_valid(self, form):
        messages.success(self.request, "Department deleted.")
        return super().form_valid(form)


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'departments/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sections'] = self.object.sections.all().select_related('academic_year')
        ctx['faculty_members'] = self.object.faculty_members.filter(is_active=True).select_related('user')
        ctx['subjects'] = self.object.subjects.filter(is_active=True)
        return ctx


# ─── AcademicYear CRUD ───────────────────────────────────────────────────────

class AcademicYearListView(LoginRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'departments/academic_year_list.html'
    context_object_name = 'academic_years'


class AcademicYearCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'departments/academic_year_form.html'
    success_url = reverse_lazy('departments:academic_year_list')

    def form_valid(self, form):
        messages.success(self.request, "Academic year created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Academic Year'
        ctx['action'] = 'Create'
        return ctx


class AcademicYearUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'departments/academic_year_form.html'
    success_url = reverse_lazy('departments:academic_year_list')

    def form_valid(self, form):
        messages.success(self.request, "Academic year updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Academic Year'
        ctx['action'] = 'Update'
        return ctx


class AcademicYearDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = AcademicYear
    template_name = 'departments/academic_year_confirm_delete.html'
    success_url = reverse_lazy('departments:academic_year_list')

    def form_valid(self, form):
        messages.success(self.request, "Academic year deleted.")
        return super().form_valid(form)


# ─── Section CRUD ────────────────────────────────────────────────────────────

class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = 'departments/section_list.html'
    context_object_name = 'sections'
    paginate_by = 20

    def get_queryset(self):
        qs = Section.objects.select_related('department', 'academic_year')
        dept = self.request.GET.get('department')
        year = self.request.GET.get('academic_year')
        if dept:
            qs = qs.filter(department_id=dept)
        if year:
            qs = qs.filter(academic_year_id=year)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from departments.models import Department
        ctx['departments'] = Department.objects.all()
        ctx['academic_years'] = AcademicYear.objects.all()
        return ctx


class SectionCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'departments/section_form.html'
    success_url = reverse_lazy('departments:section_list')

    def form_valid(self, form):
        messages.success(self.request, "Section created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Section'
        ctx['action'] = 'Create'
        return ctx


class SectionUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'departments/section_form.html'
    success_url = reverse_lazy('departments:section_list')

    def form_valid(self, form):
        messages.success(self.request, "Section updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Section'
        ctx['action'] = 'Update'
        return ctx


class SectionDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Section
    template_name = 'departments/section_confirm_delete.html'
    success_url = reverse_lazy('departments:section_list')

    def form_valid(self, form):
        messages.success(self.request, "Section deleted.")
        return super().form_valid(form)
