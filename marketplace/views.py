from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request , 'index.html')

def auth_view(request):
    return render(request , 'auth.html')

def terms_view(request):
    return render(request , 'terms.html')

def privacy_view(request):
    return render(request , 'privacy.html')