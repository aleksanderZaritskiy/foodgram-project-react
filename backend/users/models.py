from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram import constants, validators


class User(AbstractUser):
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    USERNAME_FIELD = 'email'
    username = models.CharField(
        'Логин',
        help_text='Укажите ваш псевдоним',
        max_length=constants.LENGTH_LOGIN,
        validators=(UnicodeUsernameValidator(),),
        error_messages={'max_length': "больше 150 символов"},
        unique=True,
    )
    email = models.EmailField(
        'Почта',
        help_text=(
            'Укажите свою электронную почту. '
            'На неё вам придёт письмо с кодом подтвержедния'
        ),
        max_length=constants.LENGTH_EMAIL,
        error_messages={'max_length': "не валидный имейл больше 254 символов"},
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        help_text='Укажите имя',
        max_length=constants.LENGTH_NAME,
        validators=(validators.validate_name,),
    )
    last_name = models.CharField(
        'Фамилия',
        help_text='Укажите фамилию',
        max_length=constants.LENGTH_NAME,
        validators=(validators.validate_name,),
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('subscriber')),
                name='Нельзя подписаться на себя',
            )
        ]
