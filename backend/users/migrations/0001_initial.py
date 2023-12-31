# Generated by Django 3.2.16 on 2023-12-04 13:16

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'password',
                    models.CharField(max_length=128, verbose_name='password'),
                ),
                (
                    'last_login',
                    models.DateTimeField(
                        blank=True, null=True, verbose_name='last login'
                    ),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='date joined',
                    ),
                ),
                (
                    'username',
                    models.CharField(
                        error_messages={'max_length': 'больше 150 символов'},
                        help_text='Укажите ваш псевдоним',
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name='Логин',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        error_messages={
                            'max_length': 'не валидный имейл больше 254 символов'
                        },
                        help_text='Укажите свою электронную почту. На неё вам придёт письмо с кодом подтвержедния',
                        max_length=254,
                        unique=True,
                        verbose_name='Почта',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(
                        help_text='Укажите имя',
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^[а-яА-ЯёЁa-zA-Z]*$',
                                'Поле должно содержать только буквы кириллицы/латиницы',
                            )
                        ],
                        verbose_name='Имя',
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        help_text='Укажите фамилию',
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^[а-яА-ЯёЁa-zA-Z]*$',
                                'Поле должно содержать только буквы кириллицы/латиницы',
                            )
                        ],
                        verbose_name='Фамилия',
                    ),
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'ordering': ('-id',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'subscriber',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='subscriber',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='user',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(
                fields=('user', 'subscriber'), name='unique_user_subscriber'
            ),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('user', django.db.models.expressions.F('subscriber')),
                    _negated=True,
                ),
                name='Нельзя подписаться на себя',
            ),
        ),
    ]
