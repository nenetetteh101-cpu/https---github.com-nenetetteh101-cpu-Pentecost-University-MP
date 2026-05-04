from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('listings/', views.listings, name='listings'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('create/', views.create_listing, name='create'),
    # 1. The "Save" Handshake: Matches fetch('/listings/api/create/')
    # This receives the Cloudinary URL string and form data
    path('api/create/', views.create_listing_api, name='create_api'),

    # 2. The "Pull" Handshake: Matches fetch('/listings/api/my-listings/')
    # This sends back the list of listings with their URL strings
    path('api/listings/me/', views.get_my_listings, name='my_listings_api'),
    
    # 3. Page Routes: To serve the actual HTML files
    
]
