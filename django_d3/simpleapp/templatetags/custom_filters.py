from django import template

register = template.Library()


# Регистрируем фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблона, а не простая функция.

@register.filter()
def currency(value):
    """
    value: значение, к которому нуо применить фильтр

    """
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} P'
