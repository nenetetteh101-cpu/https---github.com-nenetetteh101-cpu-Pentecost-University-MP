
import re
import time


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignUpForm

# Create your views here.
def home_view(request):
    return render(request , 'index.html')

def auth_view(request):
    return render(request , 'auth.html')

def terms_view(request):
    return render(request , 'terms.html')

def privacy_view(request):
    return render(request , 'privacy.html'),
def dashboard_view(request):
    return render(request , 'dashboard.html'),


# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .forms import LoginForm, SignUpForm # Import the forms we made above

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('identifier')
            password = form.cleaned_data.get('password')

            # Check if user is logging in with Email or Username
            user = None
            if "@" in identifier:
                try:
                    user_obj = User.objects.get(email=identifier)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            else:
                user = authenticate(username=identifier, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_view')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        
    # If it's a GET request or form is invalid
    return render(request, 'auth.html', {'active_tab': 'login'})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user but don't save to DB yet
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # IMMEDIATELY Log the user in after sign up
            login(request, user)
            messages.success(request, f"Welcome to the campus, {user.first_name}!")
            return redirect('dashboard_view')
        else:
            # Pass errors back to the template
            return render(request, 'auth.html', {
                'active_tab': 'signup',
                'signup_errors': form.errors,
                'signup_form_data': request.POST
            })
    return render(request, 'auth.html', {'active_tab': 'signup'})

@login_required # Prevents non-logged in users from seeing the dashboard
def dashboard_view(request):
    return render(request, 'dashboard.html')