# Generated by Django 3.0.6 on 2020-05-10 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_profile_subscibers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='subscibers',
            new_name='subscribers',
        ),
    ]
