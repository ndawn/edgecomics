import locale
import datetime

from django import template


register = template.Library()


correct = lambda d: d + 'а' if d.endswith('т') else d[:-1] + 'я'


@register.filter(name='format_date')
def format_date(value, day=True):
    if value is None:
        return '–'
    else:
        if isinstance(value, tuple):
            value = value[0]
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        d = value.strftime('%d ') if day else ''
        m = (correct(value.strftime('%B')) if day else value.strftime('%B')).lower()
        res = d + m + value.strftime(' %Y')
        locale.setlocale(locale.LC_TIME, '')
        return res


@register.filter(name='format_timestamp')
def format_timestamp(value):
    date = datetime.datetime.fromtimestamp(value)
    m = correct(date.strftime('%B')).lower()
    return date.strftime('%d ') + m + date.strftime(' %Y %H:%M')
