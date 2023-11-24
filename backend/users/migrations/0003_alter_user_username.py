# Generated by Django 3.2.16 on 2023-11-13 18:49

from django.db import migrations, models
import foodgram.validators


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_auto_20231113_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                blank=True,
                max_length=150,
                unique=True,
                validators=[foodgram.validators.validate_name],
                verbose_name='Логин',
            ),
        ),
    ]
