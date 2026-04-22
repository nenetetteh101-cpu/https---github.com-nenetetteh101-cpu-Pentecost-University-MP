"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Base app (includes: home, about, help, terms, privacy, safety, contact)
    path('', include('Base_app.urls')),



        # Authentication
    path('auth/', include('Auth_app.urls')),
    
    # Main apps
  
]

# Media & Static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)