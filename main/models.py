from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class MusicTrack(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name="track", on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name="track_likes")
    dislikes = models.ManyToManyField(User, related_name="track_dislikes")
    comments = models.ManyToManyField(TrackComment, related_name="track_comments")
    reports = models.ManyToManyField(TrackComment, related_name="track_reports")
    settings = models.ManyToManyField(TrackSettings)

class TrackSettings(models.Model):
    allow_comments = models.BooleanField()
    allow_rating = models.BooleanField()
    allow_reusing = models.BooleanField()

class TrackComment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField()
    checked_by_author = models.BooleanField()