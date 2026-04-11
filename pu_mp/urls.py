"""
URL configuration for pu_mp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from marketplace.views import home_view
from marketplace import views
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name='home'),
    path('home/',views.home_view,name='home_view'),
    path('auth/',views.auth_view,name='Auth_view'),
    path('terms/',views.terms_view,name='terms_view'),
    path('privacy/',views.privacy_view,name='privacy_view'),
    path('auth/login/', never_cache(views.login_view), name='login_view'),
    path('auth/signup/', views.signup_view, name='signup_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('safety/', views.safety_view, name='safety_view'),
    path('about/', views.about_view, name='about_view'),
    path('help/', views.help_view, name='help_view'),
    path('chat/', views.chat_view, name='chat_view'),
    path('reels/', views.reels_view, name='reels_view'),
    path('settings/', views.settings_view, name='settings_view'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('listings/', views.listings_view, name='listings_view'),
    path('orders/', views.orders_view, name='orders_view'),
    path('payments/', views.payments_view, name='payments_view'),
    path('profile/', views.profile_view, name='profile_view'),
    path('dashboard/services/', views.dashboard_services_view, name='dashboard_services_view'),
    path('dashboard/products/', views.dashboard_products_view, name='dashboard_products_view'),

    # Django built-in password reset flow
    path('auth/password/', include('django.contrib.auth.urls')),



    # Matches the redirect name
    # ... other paths
    # ... other paths

]








