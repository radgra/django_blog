from django import template

register = template.Library()

@register.inclusion_tag('core/includes/navigation.html', takes_context=True)
def navigation(context):
    return context