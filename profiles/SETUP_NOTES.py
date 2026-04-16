# ════════════════════════════════════════════════════════
#  settings.py additions
# ════════════════════════════════════════════════════════

INSTALLED_APPS = [
    # ... existing apps ...
    'profiles',       # your profiles app
    'listings',       # your listings app (assumed)
    'reviews',        # your reviews app (assumed)
]

# Media files (profile pictures)
import os
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ════════════════════════════════════════════════════════
#  project urls.py (root URLconf)
# ════════════════════════════════════════════════════════

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # ... other patterns ...
    path('profile/', include('profiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ════════════════════════════════════════════════════════
#  Migration commands  (run these in terminal)
# ════════════════════════════════════════════════════════

# python manage.py makemigrations profiles
# python manage.py migrate

# Install Pillow for ImageField support
# pip install Pillow
