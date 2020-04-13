from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

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

    author = models.ForeignKey(User, models.CASCADE, "comments")
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
    :param listeners: список юзеров, послушавших трек
    '''

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(User, models.CASCADE, "tracks")
    creation_date = models.DateTimeField()
    likes = models.ManyToManyField(User, "likes")
    dislikes = models.ManyToManyField(User, "dislikes")
    comments = models.ManyToManyField(TrackComment, "comments")
    reports = models.ManyToManyField(TrackComment, "reports")
    listeners = models.ManyToManyField(User, "listened_tracks")

    def to_dict(self):
        '''
        Переводит модель трека в словарь
        (ManyToMany поля недоступны, ForeignKey заменены на id)

        :rtype: dict
        '''

        return model_to_dict(self, fields=('id', 'name', 'desc', 'author', 'creation_date', 'settings'))


class TrackSettings(models.Model):
    '''
    Настройки публикации проекта

    :param track: музыкальный трек
    :param allow_comments: разрешены ли комментарии
    :param allow_rating: разрешены ли лайки / дизлайки
    :param allow_reusing: разрешено ли свободное использование
    '''

    track = models.OneToOneField(
        MusicTrack, models.CASCADE,
        primary_key=True, related_name='settings'
    )

    allow_comments = models.BooleanField()
    allow_rating = models.BooleanField()
    allow_reusing = models.BooleanField()
