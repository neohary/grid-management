from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def get_value(context,code):
    request = context['request']
    result = eval(code)
    return result