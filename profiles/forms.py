from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import re

from .models import UserProfile, FACULTY_CHOICES, LOCATION_CHOICES, VISIBILITY_CHOICES, MEETUP_CHOICES


class ProfileUpdateForm(forms.ModelForm):
    """Handles bio, faculty, location, phone, profile pic."""

    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio', 'faculty', 'location', 'phone']
        widgets = {
            'bio': forms.Textarea(attrs={'maxlength': 200, 'rows': 3}),
            'faculty': forms.Select(choices=[('', '— Select faculty —')] + list(FACULTY_CHOICES)),
            'location': forms.Select(choices=[('', '— Select location —')] + list(LOCATION_CHOICES)),
            'phone': forms.TextInput(attrs={'placeholder': '+233 xx xxx xxxx'}),
        }

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '')
        if len(bio) > 200:
            raise ValidationError('Bio cannot exceed 200 characters.')
        return bio


class NameUpdateForm(forms.ModelForm):
    """Handles first_name + last_name on the User model."""

    first_name = forms.CharField(max_length=30, required=True)
    last_name  = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned = super().clean()
        first = cleaned.get('first_name', '').strip()
        if not first:
            raise ValidationError('First name is required.')
        return cleaned


USERNAME_RE = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._]*[a-zA-Z0-9]$')
MAX_USERNAME_CHANGES = 3


class UsernameUpdateForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_username(self):
        new_username = self.cleaned_data['username'].strip()

        if not USERNAME_RE.match(new_username):
            raise ValidationError(
                'Invalid username — use letters, numbers, dots or underscores only. '
                'No spaces, leading/trailing special chars, or consecutive dots/underscores.'
            )
        if '..' in new_username or '__' in new_username:
            raise ValidationError('Username cannot contain consecutive dots or underscores.')

        # Check uniqueness (exclude self)
        qs = User.objects.filter(username=new_username)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise ValidationError('That username is already taken.')

        # Check cooldown & lifetime limit
        profile = self.user.profile
        if new_username == self.user.username:
            return new_username  # no change, skip checks

        if profile.username_change_count >= MAX_USERNAME_CHANGES:
            raise ValidationError('You have used all 3 lifetime username changes.')

        if profile.username_locked:
            raise ValidationError(
                f'You can change your username again in {profile.username_days_left} day(s).'
            )

        return new_username


class AccountSettingsForm(forms.ModelForm):
    """Notification & privacy settings."""

    class Meta:
        model = UserProfile
        fields = [
            'notify_messages', 'notify_orders', 'notify_price_drops', 'notify_promos',
            'is_online', 'profile_visibility', 'auto_renew', 'preferred_meetup',
        ]
        widgets = {
            'profile_visibility': forms.Select(choices=VISIBILITY_CHOICES),
            'preferred_meetup':   forms.Select(choices=MEETUP_CHOICES),
        }


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']

    def clean_profile_pic(self):
        pic = self.cleaned_data.get('profile_pic')
        if pic and pic.size > 5 * 1024 * 1024:
            raise ValidationError('Photo too large — max 5 MB.')
        return pic
