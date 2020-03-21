from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def music_track_pattern_path(instance, filename):
    '''
    Возвращает путь до паттерна в папке проекта

    :param instance: модель паттерна
    :param filename: имя файла
    :rtype: str
    '''

    return "projects/{}/patterns/{}_{}".\
        format(instance.project.id, instance.id, filename)


def music_track_project_data_path(instance, filename):
    '''
    Возвращает путь до файда с данными проекта
    (настройки, инструменты и т.д.)

    :param instance: модель проекта
    :param filename: имя файла
    :rtype: str
    '''

    return "projects/{}/{}".format(instance.id, filename)


class MusicTrackPattern(models.Model):
    '''
    Модель паттерна проекта

    :param name: имя паттерна
    :paran midi: midi файл с данными паттерна
    '''

    name = models.CharField(max_length=25)
    midi = models.FileField(upload_to=music_track_pattern_path)


class MusicTrackProject(models.Model):
    '''
    Модель проекта

    :param name: имя проекта
    :param desc: описание
    :param author: автор
    :param patterns: список паттернов
    :param data: файл с данными проекта (настройки, инструменты и т.д.)
    '''

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(
        User, related_name="projects", on_delete=models.CASCADE)
    patterns = models.ManyToManyField(
        MusicTrackPattern, related_name="project")
    data = models.FileField(upload_to=music_track_project_data_path)


class TrackSettings(models.Model):
    '''
    Настройки публикации проекта

    :param allow_comments: разрешены ли комментарии
    :param allow_rating: разрешены ли лайки / дизлайки
    :param allow_reusing: разрешено ли свободное использование
    '''

    allow_comments = models.BooleanField()
    allow_rating = models.BooleanField()
    allow_reusing = models.BooleanField()


class TrackComment(models.Model):
    '''
    Модель Комментария / жалобы

    :param author: автор
    :param topic: тема
    :param content: содержание
    :param creation_date: дата создания
    :param edit_date: дата редактирования
    :param checked_by_author: просмотрен ли автором трека
    '''

    author = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField()
    checked_by_author = models.BooleanField()


class MusicTrack(models.Model):
    '''
    Модель опубликованного проекта

    :param name: имя проекта
    :param desc: описание
    :param author: автор
    :param creation_date: дата публикации
    :param likes: список юзеров, поставивших лайк
    :param dislikes: список юзеров, поставивших дизлайк
    :param comments: список комментариев
    :param reports: список жалоб
    :param settings: настройки
    '''

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(
        User, related_name="tracks", on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    likes = models.ManyToManyField(User, related_name="likes")
    dislikes = models.ManyToManyField(User, related_name="dislikes")
    comments = models.ManyToManyField(TrackComment, related_name="comments")
    reports = models.ManyToManyField(TrackComment, related_name="reports")
    settings = models.ForeignKey(TrackSettings, on_delete=models.CASCADE)
