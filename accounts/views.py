from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q

from .forms import LoginForm, UserRegistrationForm, UserUpdateForm, PasswordChangeCustomForm

User = get_user_model()


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin that allows only admin users."""
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_admin_role or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('dashboard:index')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next', 'dashboard:index')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Public self-registration — new accounts default to 'student' role.
    An admin can promote the role from the Users management page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            # Force student role on self-registration for security;
            # Admin can promote to faculty/admin from the Users page.
            if user.role not in ('student',):
                user.role = 'student'
            user.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome, {user.get_full_name() or user.username}! "
                "Your account has been created. An admin can upgrade your role if needed."
            )
            return redirect('dashboard:index')
        else:
            messages.error(request, "Please fix the errors below.")
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
                return redirect('accounts:profile')
            else:
                messages.error(request, "Current password is incorrect.")
    else:
        form = PasswordChangeCustomForm()
    return render(request, 'accounts/change_password.html', {'form': form})


class UserListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.GET.get('search')
        role = self.request.GET.get('role')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        if role:
            queryset = queryset.filter(role=role)
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_role'] = self.request.GET.get('role', '')
        ctx['role_choices'] = User.ROLE_CHOICES
        return ctx


class UserCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, "User created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add New User'
        ctx['action'] = 'Create'
        return ctx


class UserUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, "User updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Edit User'
        ctx['action'] = 'Update'
        return ctx


class UserDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, "User deleted successfully.")
        return super().form_valid(form)
