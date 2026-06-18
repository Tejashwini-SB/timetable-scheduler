from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get item from dictionary by key in templates."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter(name='mul')
def mul(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='pct')
def pct(value, total):
    try:
        return round((int(value) / int(total)) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
