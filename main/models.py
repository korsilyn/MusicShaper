from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def music_track_pattern_path(instance, filename):
    return "projects/{}/patterns/{}_{}".\
        format(instance.project.id, instance.id, filename)


def music_track_project_data_path(instance, filename):
    return "projects/{}/{}".format(instance.id, filename)


class MusicTrackPattern(models.Model):
    name = models.CharField(max_length=25)
    midi = models.FileField(upload_to=music_track_pattern_path)


class MusicTrackProject(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    patterns = models.ManyToManyField(MusicTrackPattern, related_name="project")
    data = models.FileField(upload_to=music_track_project_data_path)
