# Generated by Django 3.0 on 2020-05-23 14:44

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200515_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musictrack',
            name='reports',
        ),
        migrations.AddField(
            model_name='musictrack',
            name='claims',
            field=models.ManyToManyField(related_name='claims', to='main.TrackComment'),
        ),
        migrations.AlterField(
            model_name='musicinstrument',
            name='json_settings',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='musicinstrumenteffect',
            name='json_settings',
            field=jsonfield.fields.JSONField(),
        ),
    ]