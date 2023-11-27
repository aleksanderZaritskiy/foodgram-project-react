import re

from django.core.exceptions import ValidationError


def validate_name(data):
    """Валидация имени, фамилии"""
    for char in data:
        if not char.isalpha() and not char.isdigit():
            raise ValidationError(
                (
                    'Недопустимый символ, '
                    'используйте только латинские буквы и цифры'
                )
            )


def validate_time(data):
    """Валидация времени приготовления"""
    if data < 1:
        raise ValidationError(
            'Время приготовления рецепта не может быть меньше 1 минуты'
        )


def hex_validate(data):
    """Валидация цвета (HEX)"""
    if not re.fullmatch(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', data):
        raise ValidationError('Укажите корректный HEX цвет')
