# Generated by Django 3.2.16 on 2023-11-15 19:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('foodgram', '0011_auto_20231115_2206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='coocking_time',
            new_name='cooking_time',
        ),
    ]