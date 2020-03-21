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
    author = models.ForeignKey(
        User, related_name="projects", on_delete=models.CASCADE)
    patterns = models.ManyToManyField(
        MusicTrackPattern, related_name="project")
    data = models.FileField(upload_to=music_track_project_data_path)


class MusicTrack(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(
        User, related_name="tracks", on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name="likes")
    dislikes = models.ManyToManyField(User, related_name="dislikes")
    comments = models.ManyToManyField(TrackComment, related_name="comments")
    reports = models.ManyToManyField(TrackComment, related_name="reports")
    settings = models.ManyToManyField(TrackSettings)


class TrackSettings(models.Model):
    allow_comments = models.BooleanField()
    allow_rating = models.BooleanField()
    allow_reusing = models.BooleanField()


class TrackComment(models.Model):
    author = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField()
    checked_by_author = models.BooleanField()
