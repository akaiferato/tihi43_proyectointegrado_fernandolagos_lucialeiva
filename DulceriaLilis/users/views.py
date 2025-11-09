from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import sweetify
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserProfileForm, CustomPasswordChangeForm
from .decorators import group_required

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
                return redirect('home')  # Redirect to a home page after login
            else:
                sweetify.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    sweetify.info(request, "You have been logged out.")
    return redirect('login')  # Redirect to the login page after logout

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
            update_session_auth_hash(request, user)  # Important! Keeps the user logged in
            sweetify.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            sweetify.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})

@group_required('Administrator')
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')