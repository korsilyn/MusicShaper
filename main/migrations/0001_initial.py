# Generated by Django 3.0 on 2020-03-27 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='MusicTrackPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('color', models.CharField(max_length=25)),
                ('duration', models.FloatField()),
                ('notes', models.FileField(upload_to=main.models.music_track_pattern_path)),
            ],
        ),
        migrations.CreateModel(
            name='TrackSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_comments', models.BooleanField()),
                ('allow_rating', models.BooleanField()),
                ('allow_reusing', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TrackComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=400)),
                ('creation_date', models.DateTimeField()),
                ('edit_date', models.DateTimeField()),
                ('checked_by_author', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='', upload_to='profile_pics')),
                ('status', models.CharField(default='', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MusicTrackProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=250)),
                ('creation_date', models.DateTimeField()),
                ('timeline_data', models.FileField(upload_to=main.models.music_track_project_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('instruments', models.ManyToManyField(related_name='project', to='main.MusicInstrument')),
                ('patterns', models.ManyToManyField(related_name='project', to='main.MusicTrackPattern')),
            ],
        ),
        migrations.CreateModel(
            name='MusicTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=250)),
                ('creation_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(related_name='comments', to='main.TrackComment')),
                ('dislikes', models.ManyToManyField(related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('reports', models.ManyToManyField(related_name='reports', to='main.TrackComment')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TrackSettings')),
            ],
        ),
    ]
