from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from count_app.forms import *
from count_app.models import *
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


def home_page(request):
    return render(request, 'home.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            user = form_data.save()
            login(request, user)
            messages.success(request, f'Registration successful! Welcome, {user.username}.')
            return redirect('dashboard')  
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form_data = RegisterForm()
        
    context = {
        'form_data': form_data,
        'form_title': 'Register',
        'btn_name': 'Sign Up'
    }
    return render(request, 'base-auth.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form_data = LoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard') 
        else:
            messages.error(request, 'Invalid username or password.') 
    else:
        form_data = LoginForm()  
        
    context = {
        'form_data': form_data,
        'form_title': 'Login',
        'btn_name': 'Sign In'
    }
    return render(request, 'base-auth.html', context)


@login_required
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login_page')


@login_required
def dashboard(request):
    today = timezone.now().date()
    
    if request.method == 'POST':
        form_data = ConsumeForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Calorie entry logged successfully!')
            return redirect("dashboard")
        else:
            messages.error(request, 'Failed to log entry. Please try again.')

    calories_today = CalorieConsume.objects.filter(
        user=request.user, 
        created_at=today  
    ).aggregate(Sum('calorie_consumed'))['calorie_consumed__sum'] or 0
    
    context = {
        'calories_today': calories_today
    }
    return render(request, 'dashboard.html', context)



@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def update_profile(request):
    profile_instance, created = ProfileModel.objects.get_or_create(user=request.user)
        
    if request.method == 'POST':
        form_data = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            
            weight = float(data.weight or 0)
            height = float(data.height or 0)
            age = int(data.age or 0)
            
            if height > 0 and weight > 0:
                if data.gender == "Male":
                    data.bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
                else:
                    data.bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)            
                height_m = height / 100
                data.bmi = round(weight / (height_m ** 2), 1)
                
            data.save()
            messages.success(request, 'Profile details successfully saved!')
            return redirect("profile")
    else:
        form_data = ProfileForm(instance=profile_instance)
        
    context = {
        'form_data': form_data,
        'form_title': 'Update Profile',
        'btn_name': 'Profile'
    }
    return render(request, 'master/base-form.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form_data = MyPasswordChangeForm(request.user, request.POST)
        if form_data.is_valid():
            user = form_data.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully updated!')
            return redirect('profile') 
        else:
            messages.error(request, 'Check the mistakes!')
    else:
        form_data = MyPasswordChangeForm(request.user)
    
    context = {
        'form_data': form_data,
        'form_title': 'Change Password',
        'btn_name': 'Update Password'
    }
    return render(request, 'master/base-form.html', context) 


@login_required
def consume_profile(request):
    if request.method == 'POST':
        form_data = ConsumeForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Calorie entry logged successfully!')
            return redirect("dashboard")
    else:
        form_data = ConsumeForm()
        
    context = {
        'form_data': form_data,
        'form_title': 'Consumed Calorie',
        'btn_name': 'Add'
    }
    return render(request, 'master/base-form.html', context)
