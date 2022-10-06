from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def get_context_processor(context,context_processors):
    request_context = context[context_processors]
    
    return request_context