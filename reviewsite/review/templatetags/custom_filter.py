from django import template

register = template.Library()


@register.simple_tag
def query_replace(request, field, value):
    params_dict = request.GET.copy()
    params_dict[field] = value
    return params_dict.urlencode()
