# execution/templatetags/dict_extras.py
# This file lets us do {{ my_dict|get_key:variable }} in templates
# Django doesn't support dict[variable] lookups natively in templates

from django import template

register = template.Library()

@register.filter
def get_key(dictionary, key):
    if dictionary is None:
        return "—"
    return dictionary.get(key, "—")






