# Generated by Django 3.0 on 2020-05-30 13:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200517_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicnote',
            name='length',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
