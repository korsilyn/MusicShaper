from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def music_instrument_path(instance, filename):
    return 'music_track_projects/{}/instruments/id_{}__{}'.\
        format(instance.project.id, instance.id, filename)

class MusicInstrument(models.Model):
    name = models.CharField(max_length=64)
    sound_file = models.FileField(upload_to=music_instrument_path, null=True)
    sound_source = models.CharField(max_length=16, null=True)
    effects = models.CharField()

class MusicTrackProject(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    instruments = models.ManyToManyField(MusicInstrument, related_name="project")
