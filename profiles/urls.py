from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.profile_view,    name='profile'),

    # Profile edits
    path('update/name/',       views.update_name,     name='update_name'),
    path('update/username/',   views.update_username, name='update_username'),
    path('update/profile/',    views.update_profile,  name='update_profile'),
    path('update/avatar/',     views.upload_avatar,   name='upload_avatar'),
    path('update/settings/',   views.update_settings, name='update_settings'),

    # Online status toggle
    path('toggle-online/',     views.toggle_online,   name='toggle_online'),

    # Account lifecycle
    path('deactivate/',        views.deactivate_account, name='deactivate_account'),
    path('reactivate/',        views.reactivate_account, name='reactivate_account'),
    path('delete/',            views.delete_account,     name='delete_account'),

    # Logout
    path('logout/',            views.logout_view,     name='logout'),
]