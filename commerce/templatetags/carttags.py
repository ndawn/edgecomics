from django import template
from commerce.models import Category


register = template.Library()


@register.filter(name='expand')
def expand(value):
    expanded = []

    if isinstance(value, Category):
        expanded.insert(0, value.title)

        while value.parent is not None:
            expanded.insert(0, value.parent.title)
            value = value.parent
    else:
        return ''

    return ' > '.join(expanded)
