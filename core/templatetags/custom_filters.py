from django import template

register = template.Library()

@register.filter(name='format_money')
def format_money(value):
    try:
        # This takes the number, adds commas, and forces 2 decimal places
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return value