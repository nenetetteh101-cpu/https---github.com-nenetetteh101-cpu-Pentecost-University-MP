from django.shortcuts import render

# Create your views here.


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

