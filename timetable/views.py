from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.http import JsonResponse

from .models import TimeSlot, Timetable, TimetableEntry, SubjectFacultyAssignment
from .forms import (
    TimeSlotForm, TimetableForm, TimetableEntryForm,
    SubjectFacultyAssignmentForm, TimetableFilterForm, AutoScheduleForm
)
from .scheduler import SchedulerEngine
from accounts.views import AdminRequiredMixin


# ─── TimeSlot CRUD ────────────────────────────────────────────────────────────

class TimeSlotListView(LoginRequiredMixin, ListView):
    model = TimeSlot
    template_name = 'timetable/timeslot_list.html'
    context_object_name = 'timeslots'

    def get_queryset(self):
        return TimeSlot.objects.all().order_by('day', 'period_number')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        ctx['slots_by_day'] = {
            day: [s for s in ctx['timeslots'] if s.day == day]
            for day in days
        }
        return ctx


class TimeSlotCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = TimeSlot
    form_class = TimeSlotForm
    template_name = 'timetable/timeslot_form.html'
    success_url = reverse_lazy('timetable:timeslot_list')

    def form_valid(self, form):
        messages.success(self.request, "Time slot created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add Time Slot'
        ctx['action'] = 'Create'
        return ctx


class TimeSlotUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = TimeSlot
    form_class = TimeSlotForm
    template_name = 'timetable/timeslot_form.html'
    success_url = reverse_lazy('timetable:timeslot_list')

    def form_valid(self, form):
        messages.success(self.request, "Time slot updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Time Slot'
        ctx['action'] = 'Update'
        return ctx


class TimeSlotDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = TimeSlot
    template_name = 'timetable/timeslot_confirm_delete.html'
    success_url = reverse_lazy('timetable:timeslot_list')

    def form_valid(self, form):
        messages.success(self.request, "Time slot deleted.")
        return super().form_valid(form)


# ─── Timetable CRUD ──────────────────────────────────────────────────────────

class TimetableListView(LoginRequiredMixin, ListView):
    model = Timetable
    template_name = 'timetable/timetable_list.html'
    context_object_name = 'timetables'
    paginate_by = 15

    def get_queryset(self):
        qs = Timetable.objects.select_related(
            'section__department', 'academic_year', 'created_by'
        )
        dept = self.request.GET.get('department', '')
        year = self.request.GET.get('academic_year', '')
        section = self.request.GET.get('section', '')
        search = self.request.GET.get('search', '')
        if dept:
            qs = qs.filter(section__department_id=dept)
        if year:
            qs = qs.filter(academic_year_id=year)
        if section:
            qs = qs.filter(section_id=section)
        if search:
            qs = qs.filter(
                Q(section__name__icontains=search) |
                Q(section__department__name__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from departments.models import Department, AcademicYear, Section
        ctx['departments'] = Department.objects.all()
        ctx['academic_years'] = AcademicYear.objects.all()
        ctx['sections'] = Section.objects.select_related('department').all()
        ctx['search'] = self.request.GET.get('search', '')
        return ctx


class TimetableCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'timetable/timetable_form.html'
    success_url = reverse_lazy('timetable:timetable_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Timetable created. Now add entries.")
        response = super().form_valid(form)
        return redirect('timetable:timetable_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Create Timetable'
        ctx['action'] = 'Create'
        return ctx


class TimetableDetailView(LoginRequiredMixin, DetailView):
    model = Timetable
    template_name = 'timetable/timetable_detail.html'
    context_object_name = 'timetable'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        entries = self.object.entries.select_related(
            'time_slot', 'subject', 'faculty__user', 'classroom'
        ).order_by('time_slot__day', 'time_slot__period_number')

        # Build grid: {day: {period: entry}}
        grid = {day: {} for day in days}
        for entry in entries:
            grid[entry.time_slot.day][entry.time_slot.period_number] = entry

        all_slots = TimeSlot.objects.order_by('day', 'period_number')
        periods = sorted(set(s.period_number for s in all_slots))
        slot_labels = {
            s.period_number: s for s in all_slots if s.day == 'Monday'
        }

        ctx['grid'] = grid
        ctx['days'] = days
        ctx['periods'] = periods
        ctx['slot_labels'] = slot_labels
        ctx['all_slots'] = all_slots
        ctx['entries'] = entries
        ctx['entry_count'] = entries.count()
        return ctx


class TimetableUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'timetable/timetable_form.html'

    def get_success_url(self):
        return reverse('timetable:timetable_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Timetable updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit Timetable'
        ctx['action'] = 'Update'
        return ctx


class TimetableDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Timetable
    template_name = 'timetable/timetable_confirm_delete.html'
    success_url = reverse_lazy('timetable:timetable_list')

    def form_valid(self, form):
        messages.success(self.request, "Timetable deleted.")
        return super().form_valid(form)


# ─── TimetableEntry CRUD ─────────────────────────────────────────────────────

@login_required
def entry_create(request, timetable_pk):
    timetable = get_object_or_404(Timetable, pk=timetable_pk)
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST, timetable=timetable)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.timetable = timetable
            try:
                entry.save()
                messages.success(request, "Entry added to timetable.")
                return redirect('timetable:timetable_detail', pk=timetable.pk)
            except Exception as e:
                messages.error(request, f"Conflict detected: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TimetableEntryForm(timetable=timetable)
    return render(request, 'timetable/entry_form.html', {
        'form': form,
        'timetable': timetable,
        'title': 'Add Timetable Entry',
    })


@login_required
def entry_update(request, pk):
    entry = get_object_or_404(TimetableEntry, pk=pk)
    timetable = entry.timetable
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST, instance=entry, timetable=timetable)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Entry updated.")
                return redirect('timetable:timetable_detail', pk=timetable.pk)
            except Exception as e:
                messages.error(request, f"Conflict detected: {e}")
    else:
        form = TimetableEntryForm(instance=entry, timetable=timetable)
    return render(request, 'timetable/entry_form.html', {
        'form': form,
        'timetable': timetable,
        'entry': entry,
        'title': 'Edit Timetable Entry',
    })


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(TimetableEntry, pk=pk)
    timetable_pk = entry.timetable.pk
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Entry removed.")
    return redirect('timetable:timetable_detail', pk=timetable_pk)


# ─── Auto-Scheduler ──────────────────────────────────────────────────────────

@login_required
def auto_schedule(request):
    if request.method == 'POST':
        form = AutoScheduleForm(request.POST)
        if form.is_valid():
            section = form.cleaned_data['section']
            academic_year = form.cleaned_data['academic_year']
            overwrite = form.cleaned_data['overwrite_existing']
            engine = SchedulerEngine(section, academic_year)
            timetable, success = engine.auto_schedule(overwrite=overwrite)

            for warning in engine.warnings:
                messages.warning(request, warning)
            for error in engine.errors:
                messages.error(request, error)

            if success:
                messages.success(
                    request,
                    f"Timetable auto-generated successfully for {section}! "
                    f"({timetable.entries.count()} entries created)"
                )
                return redirect('timetable:timetable_detail', pk=timetable.pk)
            else:
                messages.error(request, "Auto-scheduling failed. Please review errors above.")
    else:
        form = AutoScheduleForm()
    return render(request, 'timetable/auto_schedule.html', {'form': form, 'title': 'Auto-Generate Timetable'})


# ─── Subject-Faculty Assignments ─────────────────────────────────────────────

class AssignmentListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    model = SubjectFacultyAssignment
    template_name = 'timetable/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 20

    def get_queryset(self):
        return SubjectFacultyAssignment.objects.select_related(
            'subject', 'faculty__user', 'section', 'academic_year'
        ).order_by('-assigned_at')


class AssignmentCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = SubjectFacultyAssignment
    form_class = SubjectFacultyAssignmentForm
    template_name = 'timetable/assignment_form.html'
    success_url = reverse_lazy('timetable:assignment_list')

    def form_valid(self, form):
        messages.success(self.request, "Subject-Faculty assignment created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Assign Subject to Faculty'
        ctx['action'] = 'Assign'
        return ctx


class AssignmentDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = SubjectFacultyAssignment
    template_name = 'timetable/assignment_confirm_delete.html'
    success_url = reverse_lazy('timetable:assignment_list')

    def form_valid(self, form):
        messages.success(self.request, "Assignment removed.")
        return super().form_valid(form)
