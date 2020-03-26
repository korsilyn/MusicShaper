# Generated by Django 3.0 on 2020-03-23 13:27

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicInstrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('settings', models.FileField(upload_to=main.models.music_instrument_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='musictrackpattern',
            name='instrument_id',
        ),
        migrations.AddField(
            model_name='musictrackpattern',
            name='instrument',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pattern', to='main.MusicInstrument'),
            preserve_default=False,
        ),
    ]
