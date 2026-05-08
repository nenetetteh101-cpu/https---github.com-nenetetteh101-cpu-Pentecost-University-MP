import django
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile 
from django.views.decorators.http import require_POST 
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

from django.contrib import messages
from Listings_app.models import Listing 
import json



# Create your views here.

@never_cache

@login_required(login_url='auth:auth_view')
def profile(request):
    """
    User Profile Page
    GET /profile/profile/
    
    Displays:
    - User profile information
    - Avatar and basic details
    - Reputation and ratings
    - Activity history
    - Link to profile settings
    """
    context = {
        'page_title': 'My Profile - PU-Marketplace',
        'page_description': 'View and manage your profile information.',
        # Add any additional context data needed for the profile page here
    }
    return render(request, 'profile/profile.html', context)

@login_required(login_url='auth:auth_view')
def settings(request):
    """
    Profile Settings Page
    GET /profile/settings/
    
    Displays:
    - Account settings
    - Privacy settings
    - Notification preferences
    - Security settings
    """
    context = {
        'page_title': 'Settings - PU-Marketplace',
        'page_description': 'Manage your account settings.',
    }
    return render(request, 'profile/settings.html', context)





@login_required(login_url='auth:auth_view')
@never_cache
def get_my_profile(request):
    """Sends DB data to the frontend on load."""
    
    profile, created = Profile.objects.get_or_create(user=request.user)
    return JsonResponse({
        'username': request.user.username,
        'name': request.user.get_full_name() or request.user.username,
        'bio': profile.bio or "",
        'faculty': profile.faculty or "",
        'location': profile.location or "",
        'phone': profile.phone or "",
        'avatarSrc': profile.avatar_url or "", # This is the unique image link
    })
    
    return JsonResponse({
        'username': request.user.username,
        # 'name' is what kills the "KA" (Kadeer Ahmed) initials
        'name': request.user.get_full_name() or request.user.username,
        'bio': profile.bio or "",
        'avatarSrc': profile.avatar_url or "", # Your Cloudinary or image link
    })
    
   

    # This line is the fix: it fetches the profile or creates one if missing
  

# Profile_app/views.py
# Ensure your Profile model is imported








@login_required(login_url='auth:auth_view')
@require_POST
def update_profile_api(request):
    """Receives data and Cloudinary links to save in DB."""
    try:
        data = json.loads(request.body)
        p = request.user.profile
        p.bio = data.get('bio', '')
        p.faculty = data.get('faculty', '')
        p.location = data.get('location', '')
        p.phone = data.get('phone', '')
        if data.get('avatarSrc'):
            p.avatar_url = data.get('avatarSrc')
        p.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error'}, status=400)


# Ensure your Listing model is imported


def logout_view(request):
    logout(request)
    return redirect('auth:auth_view') # Standard redirect works for logout

@login_required
def deactivate_account(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete() # This deletes listings too due to CASCADE
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

