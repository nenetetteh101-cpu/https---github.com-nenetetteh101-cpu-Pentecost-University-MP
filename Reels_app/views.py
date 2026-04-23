from django.shortcuts import render

# Create your views here.


def reels(request):
    """
    Reels/Video Feed Page
    GET /reels/reels/
    
    Displays:
    - Short video reels
    - Video recommendations
    - Like and share options
    """
    context = {
        'page_title': 'Reels - PU-Marketplace',
        'page_description': 'Discover trending items and stories on campus.',
    }
    return render(request, 'reels/reels.html', context)
