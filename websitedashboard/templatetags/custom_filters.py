from django import template

register = template.Library()

@register.filter
def indian_currency(value):
    try:
        value = int(value)
        s = str(value)[::-1]
        result = ''
        for i in range(len(s)):
            if i == 3 or (i > 3 and (i - 1) % 2 == 0):
                result += ','
            result += s[i]
        return result[::-1]
    except:
        return value
