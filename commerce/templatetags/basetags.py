from django import template


register = template.Library()


@register.filter(name='mod')
def mod(value, div):
    return value % div


@register.filter(name='multiply')
def multiply(value, mul):
    return value * mul


@register.filter(name='rub')
def rub(value):
    return str(value) + 'р.'
