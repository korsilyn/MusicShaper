from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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


class MusicInstrument(models.Model):
    '''
    Абстрактная модель музыкального инстурмента

    :param name: имя инструмента (из библиотеки Tone.js)
    :param editor_name: имя инструмента в редакторе
    :param project: проект
    '''

    class Meta:
        abstract = True

    name = models.CharField(max_length=25)
    editor_name = models.CharField(max_length=25)
    project = models.ForeignKey(
        MusicTrackProject, models.CASCADE, "instruments"
    )


class MusicInstrumentEffect(models.Model):
    '''
    Абстрактная модель эффекта музыкального инструмента
    (эхо, искажение и т.д.)

    :param instrument: музыкальный инструмент
    '''

    class Meta:
        abstract = True

    instrument = models.ForeignKey(MusicInstrument, models.CASCADE, "effects")


class MusicTrackPattern(models.Model):
    '''
    Модель паттерна проекта

    :param name: имя паттерна
    :param color: цвет паттерна в редакторе
    :param duration: продолжительность
    '''

    name = models.CharField(max_length=25)
    project = models.ForeignKey(MusicTrackProject, models.CASCADE, "patterns")
    color = models.CharField(max_length=25)
    duration = models.FloatField()


class MusicNote(models.Model):
    '''
    Модель музыкальной ноты в паттерне

    :param pattern: паттерн
    :param position: момент времени, в который должна играть нота
    :param duration: длительность ноты
    :param notation: буквенная нотация ноты
    :param octave: октава
    '''

    NOTATION_CHOICES = [
        (1,  'C'),  (2, 'C#'),
        (3,  'D'),  (4, 'D#'),
        (5,  'E'),
        (6,  'F'),  (7,  'F#'),
        (8,  'G'),  (9,  'G#'),
        (10, 'A'),  (11, 'A#'),
        (12, 'B'),
    ]

    pattern = models.ForeignKey(MusicTrackPattern, models.CASCADE, "notes")
    position = models.FloatField(validators=[MinValueValidator(0)])
    duration = models.FloatField(validators=[MinValueValidator(0.05)])
    notation = models.PositiveIntegerField(choices=NOTATION_CHOICES)
    octave = models.PositiveIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(7)]
    )


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
