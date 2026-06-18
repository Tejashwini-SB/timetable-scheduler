from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Subject
from .forms import SubjectForm
from accounts.views import AdminRequiredMixin


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 15

    def get_queryset(self):
        qs = Subject.objects.select_related('department')
        search = self.request.GET.get('search', '')
        dept = self.request.GET.get('department', '')
        stype = self.request.GET.get('type', '')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(code__icontains=search))
        if dept:
            qs = qs.filter(department_id=dept)
        if stype:
            qs = qs.filter(subject_type=stype)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from departments.models import Department
        ctx['departments'] = Department.objects.all()
        ctx['type_choices'] = Subject.SUBJECT_TYPE_CHOICES
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_dept'] = self.request.GET.get('department', '')
        ctx['selected_type'] = self.request.GET.get('type', '')
        return ctx


class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'subjects/subject_detail.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['assignments'] = self.object.assignments.select_related('faculty__user', 'section', 'academic_year')
        return ctx


class SubjectCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subjects:subject_list')

    def form_valid(self, form):
        messages.success(self.request, f"Subject '{form.instance.name}' created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Subject'
        ctx['action'] = 'Create'
        return ctx


class SubjectUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subjects:subject_list')

    def form_valid(self, form):
        messages.success(self.request, f"Subject '{form.instance.name}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Subject'
        ctx['action'] = 'Update'
        return ctx


class SubjectDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'subjects/subject_confirm_delete.html'
    success_url = reverse_lazy('subjects:subject_list')

    def form_valid(self, form):
        messages.success(self.request, "Subject deleted.")
        return super().form_valid(form)
