from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Returns a range object based on the integer value"""
    try:
        return range(int(value))  # Ensures conversion to an integer
    except ValueError:
        return range(0)  # If value is invalid, return an empty range
