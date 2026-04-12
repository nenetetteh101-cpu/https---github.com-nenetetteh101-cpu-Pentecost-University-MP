
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
    return render(request , 'privacy.html')

def help_view(request):
    return render(request , 'help.html')

def about_view(request):
    return render(request , 'about.html')


def safety_view(request):
    return render(request , 'safety.html')

def listings_view(request):
    return render(request , 'listings.html')

def create_listings_view(request):
    return render(request , 'create-listing.html')

def orders_view(request):
    return render(request , 'orders.html')

def payments_view(request):
    return render(request , 'payments.html')

def reels_view(request):
    return render(request , 'reels.html')

def settings_view(request):
    return render(request , 'settings.html')

def chat_view(request):
    return render(request , 'chat.html')

def wishlist_view(request):
    return render(request , 'wishlist.html')

def profile_view(request):
    return render(request , 'profile.html')

def dashboard_services_view(request):
    return render(request , 'dashboard-services.html')

def dashboard_products_view(request):
    return render(request , 'dashboard-products.html')
    





@login_required # Prevents non-logged in users from seeing the dashboard
def dashboard_view(request):
    return render(request, 'dashboard.html')


# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .forms import LoginForm, SignUpForm # Import the forms we made above
@never_cache
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
            if form.is_valid():
                # This block is redundant since we already check form.is_valid() above
                login(request, user)
                return redirect('dashboard_view')
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

# @login_required
# def profile_view(request):
#     # Django knows exactly who is logged in via request.user
#     user_profile = request.user.profile 
    
#     context = {
#         'profile': user_profile
#     }
#     return render(request, 'profile.html', context)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    # This automatically gets the profile linked to the logged-in user
    context = {
        'profile': request.user.profile,
        'user': request.user
    }
    return render(request, 'profile.html', context)


@never_cache
def auth_view(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        
        if form_type == 'login':
            # Instead of '...', call your login logic
            form = LoginForm(request.POST)
            if form.is_valid():
                identifier = form.cleaned_data.get('identifier')
                password = form.cleaned_data.get('password')
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
                    messages.error(request, "Invalid username/email or password.")
            
        elif form_type == 'signup':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)
                messages.success(request, f"Welcome, {user.first_name}!")
                return redirect('dashboard_view')
            else:
                # If signup fails, return the errors
                return render(request, 'auth.html', {'active_tab': 'signup', 'form': form})

    # Default return for GET requests or failed login
    return render(request, 'auth.html', {'active_tab': 'login'})
