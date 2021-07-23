from django import template
from django.utils.html import format_html

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


@register.simple_tag
def show_level(level_with_description: str) -> str:
    level, description = level_with_description.split("：")
    level_str = f'<span class="badge badge-info">{level}</span>（{description}）'
    return format_html(level_str)
