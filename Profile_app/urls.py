from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]
