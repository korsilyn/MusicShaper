from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms.models import model_to_dict


class Profile(models.Model):
    '''
    Модель профиля

    :param user: имя проекта
    :param desc: описание
    :param author: автор
    :param patterns: список паттернов
    :param data: файл с данными проекта (настройки, инструменты и т.д.)
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='', upload_to='profile_pics')
    status = models.CharField(max_length=100, default='')

    def to_dict(self):
        '''
        Переводит модель профиля в словарь
        (поле image считается за url файла)

        :rtype: dict
        '''

        return {
            'id': self.pk,
            'image': self.image.url if self.image else None,
            'status': self.status,
        }


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


def user_to_dict(user: User):
    '''
    Переводит модель пользователя в словарь

    :param user: модель пользователя
    :rtype: dict
    '''

    return {
        'id': user.pk,
        'username': user.username,
        'profile': user.profile.to_dict(),
    }


def music_track_project_path(instance, filename):
    '''
    Возвращает путь до файда с данными проекта
    (настройки, инструменты и т.д.)

    :param instance: модель проекта
    :param filename: имя файла
    :rtype: str
    '''

    return f'projects\\{instance.author.id}\\{instance.name}\\{filename}'


def music_track_pattern_path(instance, filename):
    '''
    Возвращает путь до паттерна в папке проекта

    :param instance: модель паттерна
    :param filename: имя файла
    :rtype: str
    '''

    return music_track_project_path(instance.project, f'patterns\\{instance.name}\\{filename}')


def music_instrument_path(instance, filename):
    '''
    Возвращает путь до настроек музыкального инструмента в папке проекта

    :param instance: модель инструмента
    :param filename: имя файла
    :rtype: str
    '''

    return music_track_project_path(instance.project, f'instruments\\{instance.name}\\{filename}')


class MusicInstrument(models.Model):
    '''
    Модель музыкального инстурмента
    '''

    name = models.CharField(max_length=25)
    settings = models.FileField(upload_to=music_instrument_path)


class MusicTrackPattern(models.Model):
    '''
    Модель паттерна проекта

    :param name: имя паттерна
    :param color: цвет паттерна в редакторе
    :param duration: продолжительность
    :paran notes: json файл с нотами
    '''

    name = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    duration = models.FloatField()
    notes = models.FileField(upload_to=music_track_pattern_path)


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
    author = models.ForeignKey(User, models.CASCADE, "projects")
    creation_date = models.DateTimeField()
    instruments = models.ManyToManyField(MusicInstrument, "project")
    patterns = models.ManyToManyField(MusicTrackPattern, "project")
    timeline_data = models.FileField(upload_to=music_track_project_path)


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
    '''

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(User, models.CASCADE, "tracks")
    creation_date = models.DateTimeField()
    likes = models.ManyToManyField(User, "likes")
    dislikes = models.ManyToManyField(User, "dislikes")
    comments = models.ManyToManyField(TrackComment, "comments")
    reports = models.ManyToManyField(TrackComment, "reports")
    settings = models.ForeignKey(TrackSettings, models.CASCADE)

    def to_dict(self):
        '''
        Переводит модель трека в словарь
        (ManyToMany поля недоступны, ForeignKey заменены на id)

        :rtype: dict
        '''

        return model_to_dict(self, fields=('id', 'name', 'desc', 'author', 'creation_date', 'settings'))
