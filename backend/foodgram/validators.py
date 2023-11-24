from django.core.exceptions import ValidationError


def validate_name(data):
    """Валидация имени me"""
    if data == 'me':
        raise ValidationError('Нельзя создать пользователя с именем "me"')


def validate_time(data):
    """Валидация времени приготовления"""
    if data < 1:
        raise ValidationError(
            'Время приготовления рецепта не может быть меньше 1 минуты'
        )
