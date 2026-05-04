from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='auth:auth_view')
def orders(request):
    """
    My Orders Page
    GET /orders/orders/
    
    Displays:
    - User's active and past orders
    - Order status and tracking
    - Order details and receipts
    - Option to reorder or contact seller
    """
    context = {
        'page_title': 'My Orders - PU-Marketplace',
        'page_description': 'Track and manage your orders.',
        # Add any additional context data needed for the orders page here
    }
    return render(request, 'Order/orders.html', context)

