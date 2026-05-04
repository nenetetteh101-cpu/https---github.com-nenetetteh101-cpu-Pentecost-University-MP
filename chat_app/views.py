from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='auth:auth_view')
def chat(request):
    """
    Chat/Messaging Page
    GET /chat/chat/
    
    Displays:
    - List of conversations
    - Chat interface
    - Message history
    """
    context = {
        'page_title': 'Messages - PU-Marketplace',
        'page_description': 'Chat with buyers and sellers.',
    }
    return render(request, 'chat/chat.html', context)
