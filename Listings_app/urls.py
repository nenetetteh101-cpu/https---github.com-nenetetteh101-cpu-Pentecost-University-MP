from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('listings/', views.listings, name='listings'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('create/', views.create_listing, name='create'),
]
