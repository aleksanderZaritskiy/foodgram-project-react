from django.core.validators import RegexValidator, MinValueValidator


def validate_time(data):
    validate = MinValueValidator(
        limit_value=1,
        message='Время приготовления не может быть меньше минуты',
    )
    return validate(data)


def validate_name(data):
    validate = RegexValidator(
        r'^[а-яА-ЯёЁa-zA-Z]*$', (
            'Поле должно содержать только буквы кириллицы/латиницы'
        ),
    )
    return validate(data)


def validate_color(data):
    validate = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{3,6})$', 
        message='Укажите корректный HEX цвет',
        code='invalid_HEX_color',
    )
    return validate(data)
