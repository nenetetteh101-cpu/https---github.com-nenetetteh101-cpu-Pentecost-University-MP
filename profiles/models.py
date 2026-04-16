from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


FACULTY_CHOICES = [
    ('engineering',          'Engineering'),
    ('computer_science',     'Computer Science'),
    ('business_admin',       'Business Administration'),
    ('medicine',             'Medicine & Health Sciences'),
    ('law',                  'Law'),
    ('natural_sciences',     'Natural Sciences'),
    ('social_sciences',      'Social Sciences'),
    ('arts_humanities',      'Arts & Humanities'),
]

LOCATION_CHOICES = [
    ('greater_accra',  'Greater Accra'),
    ('ashanti',        'Ashanti'),
    ('western',        'Western'),
    ('central',        'Central'),
    ('eastern',        'Eastern'),
    ('northern',       'Northern'),
    ('volta',          'Volta'),
    ('upper_east',     'Upper East'),
    ('upper_west',     'Upper West'),
    ('bono',           'Bono'),
]

VISIBILITY_CHOICES = [
    ('campus', 'Campus Only'),
    ('everyone', 'Everyone'),
    ('private', 'Private'),
]

MEETUP_CHOICES = [
    ('library',       'Library Foyer'),
    ('student_union', 'Student Union'),
    ('main_gate',     'Main Gate'),
    ('cafeteria',     'Cafeteria'),
]


class UserProfile(models.Model):
    user               = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic        = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio                = models.CharField(max_length=200, blank=True)
    faculty            = models.CharField(max_length=30, choices=FACULTY_CHOICES, blank=True)
    location           = models.CharField(max_length=30, choices=LOCATION_CHOICES, blank=True)
    phone              = models.CharField(max_length=20, blank=True)

    # Status / visibility
    is_online          = models.BooleanField(default=True)
    is_active_account  = models.BooleanField(default=True)   # deactivated flag
    profile_visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='campus')
    preferred_meetup   = models.CharField(max_length=20, choices=MEETUP_CHOICES, default='library')

    # Notifications
    notify_messages    = models.BooleanField(default=True)
    notify_orders      = models.BooleanField(default=True)
    notify_price_drops = models.BooleanField(default=True)
    notify_promos      = models.BooleanField(default=False)
    auto_renew         = models.BooleanField(default=True)

    # Username change tracking (stored server-side for security)
    username_change_count     = models.PositiveSmallIntegerField(default=0)
    username_last_changed     = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} profile'

    # ── helpers ────────────────────────────────────────────────────────────────

    @property
    def display_name(self):
        full = f'{self.user.first_name} {self.user.last_name}'.strip()
        return full or self.user.username

    @property
    def initials(self):
        fn = self.user.first_name.strip()
        ln = self.user.last_name.strip()
        if fn and ln:
            return (fn[0] + ln[0]).upper()
        if fn:
            return fn[:2].upper()
        return self.user.username[:2].upper()

    @property
    def username_locked(self):
        """Returns True if the 30-day cooldown is still active."""
        if not self.username_last_changed:
            return False
        return timezone.now() < self.username_last_changed + timedelta(days=30)

    @property
    def username_days_left(self):
        if not self.username_last_changed:
            return 0
        delta = self.username_last_changed + timedelta(days=30) - timezone.now()
        return max(0, delta.days)

    @property
    def username_changes_remaining(self):
        return max(0, 3 - self.username_change_count)

    @property
    def get_faculty_display_value(self):
        return dict(FACULTY_CHOICES).get(self.faculty, '')

    @property
    def get_location_display_value(self):
        return dict(LOCATION_CHOICES).get(self.location, '')

    # ── stats helpers (override with real querysets in views) ──────────────────

    def active_listings_count(self):
        return self.user.listings.filter(status='active').count()

    def sold_count(self):
        return self.user.listings.filter(status='sold').count()

    def review_count(self):
        return self.user.received_reviews.count()

    def average_rating(self):
        reviews = self.user.received_reviews.all()
        if not reviews.exists():
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)


# ── auto-create / save profile signal ─────────────────────────────────────────
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
