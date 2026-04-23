from django.shortcuts import render

# Create your views here.

#===================================================2024-06-01: Added dashboard view and template rendering
def dashboard(request):
    """
    User Dashboard
    GET /dashboard/dashboard/
    
    Displays:
    - User profile summary
    - Recent activity feed
    - Quick links to key features (post item, view messages, manage listings)
    - Personalized recommendations
    """
    context = {
        'page_title': 'Your Dashboard - PU-Marketplace',
        'page_description': 'Manage your account, view activity, and access key features.',
        # Add any additional context data needed for the dashboard here
    }
    return render(request, 'dash/dashboard.html', context)


def dashboard_services(request):
    """
    Dashboard Services Page
    GET /dashboard/services/
    
    Displays:
    - Available services
    - Service providers
    - Service listings and details
    """
    context = {
        'page_title': 'Services - PU-Marketplace',
        'page_description': 'Browse and manage services on PU-Marketplace.',
        # Add any additional context data needed for the services page here
    }
    return render(request, 'dash/dashboard-services.html', context)