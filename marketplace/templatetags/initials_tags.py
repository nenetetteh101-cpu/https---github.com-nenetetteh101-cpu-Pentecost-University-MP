# templatetags/initials_tags.py
from django import template

register = template.Library()

@register.filter
def get_initials(user):
    first = user.first_name[:1].upper()
    last = user.last_name[:1].upper()
    return f"{first}{last}"