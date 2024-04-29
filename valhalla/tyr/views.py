from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserProfileForm
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'tyr/login.html', {'form': form})


def dashboard(request):
    return render(request, 'tyr/dashboard.html')  # Add the dashboard view


class UserRegisterView(CreateView):
    template_name = 'tyr/register.html'
    form_class = CustomUserCreationForm  # Use your custom user creation form
    success_url = reverse_lazy('dashboard')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login page after logout


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'tyr/profile.html', {'form': form})


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'tyr/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')  # Redirect to password change done page


class UserPasswordResetView(PasswordResetView):
    template_name = 'tyr/password_reset.html'
    form_class = PasswordResetForm
    email_template_name = 'tyr/password_reset_email.html'
    subject_template_name = 'tyr/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')  # Redirect to password reset done page


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'tyr/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')  # Redirect to password reset complete page


def user_logout(request):
    logout(request)
    return redirect('login')
