from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

# Home view — just renders landing page
def home_view(request):
    # If user is already logged in, send to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "home.html")

# SIGNUP
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "All fields are required.")
            return redirect("home")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("home")

        # Create user and login
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, f"Welcome {username}!")
        return redirect("dashboard")  # ✅ Redirect to dashboard

    return redirect("home")

# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {username}")
            return redirect("dashboard")  
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home")

    return redirect("home")

# LOGOUT
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")  # or home

    return render(request, "logout.html")

# DASHBOARD
@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")