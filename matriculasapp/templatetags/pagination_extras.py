from django import template

register = template.Library()


@register.filter(name="range")
def filter_range(number, start=0):
    """Filter para criar um range de números para uso em templates.

    Exemplo: {{ 5|range }} produz [0, 1, 2, 3, 4]
            {{ 5|range:1 }} produz [1, 2, 3, 4, 5]
    """
    try:
        number = int(number)
        start_int = int(start)
        return range(start_int, number + start_int)
    except (ValueError, TypeError):
        return []
