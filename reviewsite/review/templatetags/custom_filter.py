from django import template

register = template.Library()


@register.simple_tag
def query_replace(request, field, value):
    params_dict = request.GET.copy()
    params_dict[field] = value
    return params_dict.urlencode()


@register.simple_tag
def color_by_count(count: int) -> str:
    if count >= 4:
        return "success"
    elif count == 3:
        return "primary"
    elif count == 2:
        return "warning"
    else:
        return "danger"
