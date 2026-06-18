from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Classroom
from .forms import ClassroomForm
from accounts.views import AdminRequiredMixin


class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = 'classrooms/classroom_list.html'
    context_object_name = 'classrooms'
    paginate_by = 15

    def get_queryset(self):
        qs = Classroom.objects.all()
        search = self.request.GET.get('search', '')
        rtype = self.request.GET.get('type', '')
        avail = self.request.GET.get('available', '')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(room_number__icontains=search) | Q(building__icontains=search))
        if rtype:
            qs = qs.filter(room_type=rtype)
        if avail == 'true':
            qs = qs.filter(is_available=True)
        elif avail == 'false':
            qs = qs.filter(is_available=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['type_choices'] = Classroom.ROOM_TYPE_CHOICES
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_type'] = self.request.GET.get('type', '')
        ctx['selected_avail'] = self.request.GET.get('available', '')
        return ctx


class ClassroomCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classrooms/classroom_form.html'
    success_url = reverse_lazy('classrooms:classroom_list')

    def form_valid(self, form):
        messages.success(self.request, f"Classroom '{form.instance.room_number}' added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Classroom'
        ctx['action'] = 'Create'
        return ctx


class ClassroomUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classrooms/classroom_form.html'
    success_url = reverse_lazy('classrooms:classroom_list')

    def form_valid(self, form):
        messages.success(self.request, f"Classroom '{form.instance.room_number}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Classroom'
        ctx['action'] = 'Update'
        return ctx


class ClassroomDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Classroom
    template_name = 'classrooms/classroom_confirm_delete.html'
    success_url = reverse_lazy('classrooms:classroom_list')

    def form_valid(self, form):
        messages.success(self.request, "Classroom deleted.")
        return super().form_valid(form)
