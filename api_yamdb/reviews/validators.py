import datetime as dt
from rest_framework.exceptions import ValidationError


def validate_year(value):
    """Функция валидации поля в модели Title."""
    current_year = dt.datetime.now().year
    if value > current_year:
        raise ValidationError('Неправильная дата')
    return value
