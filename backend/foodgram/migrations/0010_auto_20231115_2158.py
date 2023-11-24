# Generated by Django 3.2.16 on 2023-11-15 18:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodgram', '0009_auto_20231115_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='tag',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(
                related_name='recipe', to='foodgram.Tag', verbose_name='Тэг'
            ),
        ),
    ]
