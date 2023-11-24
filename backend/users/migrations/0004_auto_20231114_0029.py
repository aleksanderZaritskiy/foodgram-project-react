# Generated by Django 3.2.16 on 2023-11-13 21:29

import django.contrib.auth.validators
from django.db import migrations, models
import foodgram.validators


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                error_messages={
                    'max_length': 'не валидный имейл больше 254 символов'
                },
                help_text='Укажите свою электронную почту. На неё вам придёт письмо с кодом подтвержедния',
                max_length=254,
                unique=True,
                verbose_name='Почта',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(
                help_text='Укажите имя', max_length=150, verbose_name='Имя'
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(
                help_text='Укажите фамилию',
                max_length=150,
                verbose_name='Фамилия',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                blank=True,
                error_messages={'max_length': 'больше 150 символов'},
                help_text='Укажите ваш псевдоним',
                max_length=150,
                unique=True,
                validators=[
                    foodgram.validators.validate_name,
                    django.contrib.auth.validators.UnicodeUsernameValidator(),
                ],
                verbose_name='Логин',
            ),
        ),
    ]