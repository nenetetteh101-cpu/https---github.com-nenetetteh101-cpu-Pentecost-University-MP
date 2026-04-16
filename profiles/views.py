from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg, Count

from .models import UserProfile
from .forms import (
    ProfileUpdateForm, NameUpdateForm, UsernameUpdateForm,
    AccountSettingsForm, AvatarUploadForm,
)
app_name = 'profiles'

# ── helpers ────────────────────────────────────────────────────────────────────

def _rating_distribution(user):
    """Return list of {star, count, pct} dicts for 5→1 stars."""
    from reviews.models import Review  # adjust import path if needed
    totals = (
        Review.objects
        .filter(seller=user)
        .values('rating')
        .annotate(count=Count('rating'))
    )
    dist = {r['rating']: r['count'] for r in totals}
    total = sum(dist.values()) or 1
    return [
        {'star': s, 'count': dist.get(s, 0), 'pct': round(dist.get(s, 0) / total * 100)}
        for s in range(5, 0, -1)
    ]


# ── main profile view ──────────────────────────────────────────────────────────

@login_required
def profile_view(request):
    user    = request.user
    profile = user.profile  # created automatically by signal

    # Active listings (most recent 8 for the scroll strip)
    try:
        from listings.models import Listing
        active_listings = (
            Listing.objects
            .filter(seller=user, status='active')
            .order_by('-created_at')[:8]
        )
        listings_count = Listing.objects.filter(seller=user, status='active').count()
        sold_count     = Listing.objects.filter(seller=user, status='sold').count()
    except Exception:
        active_listings = []
        listings_count  = 0
        sold_count      = 0

    # Reviews (most recent 3 shown; full list via separate view)
    try:
        from reviews.models import Review
        recent_reviews  = Review.objects.filter(seller=user).select_related('reviewer', 'listing')[:3]
        review_stats    = Review.objects.filter(seller=user).aggregate(
            avg=Avg('rating'), total=Count('id')
        )
        avg_rating      = round(review_stats['avg'], 1) if review_stats['avg'] else None
        review_count    = review_stats['total']
        rating_dist     = _rating_distribution(user)
    except Exception:
        recent_reviews = []
        avg_rating     = None
        review_count   = 0
        rating_dist    = []

    # Username state for JS
    username_status = {
        'locked':    profile.username_locked,
        'days_left': profile.username_days_left,
        'remaining': profile.username_changes_remaining,
        'count':     profile.username_change_count,
    }

    context = {
        'profile':         profile,
        'active_listings': active_listings,
        'listings_count':  listings_count,
        'sold_count':      sold_count,
        'recent_reviews':  recent_reviews,
        'avg_rating':      avg_rating,
        'review_count':    review_count,
        'rating_dist':     rating_dist,
        'username_status': username_status,
        # forms (pre-populated)
        'profile_form':   ProfileUpdateForm(instance=profile),
        'name_form':      NameUpdateForm(instance=user),
        'settings_form':  AccountSettingsForm(instance=profile),
    }
    return render(request, 'profiles/profile.html', context)


# ── update name (inline or modal) ─────────────────────────────────────────────

@login_required
@require_POST
def update_name(request):
    form = NameUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'ok': True,
                'display_name': request.user.profile.display_name,
            })
        messages.success(request, 'Name updated ✅')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
        messages.error(request, 'Could not update name.')
    return redirect('profile')


# ── update username ────────────────────────────────────────────────────────────

@login_required
@require_POST
def update_username(request):
    form = UsernameUpdateForm(request.POST, user=request.user)
    if form.is_valid():
        new_username = form.cleaned_data['username']
        if new_username != request.user.username:
            request.user.username = new_username
            request.user.save(update_fields=['username'])
            profile = request.user.profile
            profile.username_change_count += 1
            profile.username_last_changed  = timezone.now()
            profile.save(update_fields=['username_change_count', 'username_last_changed'])

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            remaining = request.user.profile.username_changes_remaining
            return JsonResponse({
                'ok': True,
                'username': new_username,
                'remaining': remaining,
                'message': (
                    f'Username changed ✅ — {remaining} lifetime change{"s" if remaining != 1 else ""} remaining'
                    if remaining > 0 else 'Username changed ✅ — no more lifetime changes allowed'
                ),
            })
        messages.success(request, 'Username updated.')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            first_error = next(iter(form.errors.values()))[0]
            return JsonResponse({'ok': False, 'error': first_error}, status=400)
        messages.error(request, 'Could not update username.')
    return redirect('profile')


# ── update profile (bio / faculty / location / phone) ─────────────────────────

@login_required
@require_POST
def update_profile(request):
    form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'message': 'Profile updated ✅'})
        messages.success(request, 'Profile updated ✅')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
        messages.error(request, 'Could not save profile.')
    return redirect('profile')


# ── avatar upload (AJAX) ───────────────────────────────────────────────────────

@login_required
@require_POST
def upload_avatar(request):
    form = AvatarUploadForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'ok':  True,
            'url': request.user.profile.profile_pic.url,
        })
    error = next(iter(form.errors.values()))[0]
    return JsonResponse({'ok': False, 'error': error}, status=400)


# ── account settings ───────────────────────────────────────────────────────────

@login_required
@require_POST
def update_settings(request):
    form = AccountSettingsForm(request.POST, instance=request.user.profile)
    if form.is_valid():
        form.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True})
        messages.success(request, 'Settings saved.')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
    return redirect('profile')


# ── online toggle (single-field AJAX) ─────────────────────────────────────────

@login_required
@require_POST
def toggle_online(request):
    import json
    body   = json.loads(request.body)
    status = bool(body.get('online', True))
    request.user.profile.is_online = status
    request.user.profile.save(update_fields=['is_online'])
    return JsonResponse({'ok': True, 'online': status})


# ── deactivate / reactivate ────────────────────────────────────────────────────

@login_required
@require_POST
def deactivate_account(request):
    profile = request.user.profile
    profile.is_active_account = False
    profile.is_online          = False
    profile.save(update_fields=['is_active_account', 'is_online'])
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'status': 'deactivated'})
    messages.info(request, 'Your account has been deactivated.')
    return redirect('profile')


@login_required
@require_POST
def reactivate_account(request):
    profile = request.user.profile
    profile.is_active_account = True
    profile.save(update_fields=['is_active_account'])
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'status': 'active'})
    messages.success(request, 'Account reactivated ✅')
    return redirect('profile')


# ── delete account ─────────────────────────────────────────────────────────────

@login_required
@require_POST
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.info(request, 'Your account has been deleted.')
    return redirect('login')


# ── logout ─────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')
