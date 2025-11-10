from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import sweetify
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserProfileForm, CustomPasswordChangeForm, UserForm
from .decorators import group_required
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import User
from django.utils.decorators import method_decorator
import openpyxl
from django.db.models import Q

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                sweetify.success(request, f"Welcome, {username}!")
                return redirect('home')
            else:
                sweetify.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    sweetify.info(request, "You have been logged out.")
    return redirect('login')

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            sweetify.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            sweetify.success(request, "Your profile was successfully updated!")
            return redirect('profile_edit')
        else:
            sweetify.error(request, "Please correct the error below.")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            sweetify.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            sweetify.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})

@group_required('Administrador')
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

@method_decorator(group_required('Administrador'), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('groups')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(area__icontains=query) |
                Q(telephone_number__icontains=query)
            )
        
        sort_by = self.request.GET.get('sort_by', 'username')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            sort_by = f'-{sort_by}'
        
        return queryset.order_by(sort_by)

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', self.request.session.get('paginate_by', 10))
        self.request.session['paginate_by'] = paginate_by
        return paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = int(self.get_paginate_by(self.get_queryset()))
        context['sort_by'] = self.request.GET.get('sort_by', 'username')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context

@method_decorator(group_required('Administrador'), name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

@method_decorator(group_required('Administrador'), name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

@method_decorator(group_required('Administrador'), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

@method_decorator(group_required('Administrador'), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

@group_required('Administrador')
def export_users_to_excel(request):
    users = User.objects.prefetch_related('groups').all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Users"

    headers = ["Username", "First Name", "Last Name", "Email", "State", "Area", "Telephone", "Groups"]
    ws.append(headers)

    for user in users:
        groups = ", ".join([group.name for group in user.groups.all()])
        ws.append([
            user.username, 
            user.first_name, 
            user.last_name, 
            user.email, 
            user.get_state_display(), 
            user.area,
            user.telephone_number,
            groups
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    wb.save(response)

    return response