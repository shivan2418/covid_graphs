from django import template

register = template.Library()

@register.filter
def parse_var(value):
    return value.replace("_"," ").title()
