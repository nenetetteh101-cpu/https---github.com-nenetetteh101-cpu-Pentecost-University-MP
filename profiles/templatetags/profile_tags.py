from django import template

register = template.Library()


@register.filter
def get_initials(user):
    """
    Returns 2-letter initials for a User object.
    Uses first + last name if available, otherwise username.
    Usage: {{ user|get_initials }}
    """
    if not user:
        return '??'
    fn = (user.first_name or '').strip()
    ln = (user.last_name  or '').strip()
    if fn and ln:
        return (fn[0] + ln[0]).upper()
    if fn:
        return fn[:2].upper()
    return (user.username or '??')[:2].upper()


@register.filter
def star_range(rating):
    """Returns a range so templates can iterate over stars."""
    try:
        return range(int(rating))
    except (TypeError, ValueError):
        return range(0)


@register.filter
def subtract(value, arg):
    """{{ 5|subtract:rating }} for empty stars."""
    try:
        return int(value) - int(arg)
    except (TypeError, ValueError):
        return 0
