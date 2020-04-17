from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from jsonfield import JSONField


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
    author = models.ForeignKey(User, models.CASCADE, 'projects')
    creation_date = models.DateTimeField()


class JSONSetting(models.Model):
    '''
    Абстрактная модель настройки в формате json

    :param name: имя настройки
    :param data: данные настройки в json
    '''

    class Meta:
        abstract = True

    name = models.CharField(max_length=25)
    data = JSONField()


class ModelWithSettings(models.Model):
    '''
    Абстрактная модель *кхм* модели, у которой
    есть список настроек (JSONSetting)

    У класса дочерней модели также появляется метод
    define, с помощью которого можно задать стандартные
    настройки для определённого 'типа' объекта модели
    '''

    class Meta:
        abstract = True

    def __init_subclass__(cls):
        super().__init_subclass__()
        setattr(cls, 'DEFINITIONS', dict())

    @classmethod
    def define(cls, definition_name: str, default_settings: dict):
        '''
        Объявляет новый тип модели со стандартными настройками

        :param definition_name: имя нового типа
        :param default_settings: словарь со стандартными настройками
        '''

        if definition_name in cls.DEFINITIONS:
            raise NameError(f'definition {definition_name} already exists')
        cls.DEFINITIONS[definition_name] = default_settings.copy()

    def set_default_settings(self):
        '''
        Создаёт новые объекты стандартных настроек
        '''

        if self.type not in self.DEFINITIONS:
            raise NameError(f'type {self.type} is not defined')
        for sname, json_args in self.DEFINITIONS[self.type].items():
            self.settingModel.objects.create(
                name=sname,
                data=json_args,
                **{self.settingRelatedName: self}
            )

    def __init__(self, settingModel, related_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settingModel = settingModel
        self.settingRelatedName = related_name


class MusicInstrument(ModelWithSettings):
    '''
    Модель музыкального инстурмента

    :param name: имя инструмента в редакторе
    :param type: тип инструмента (из библиотеки Tone.js)
    :param project: проект
    '''

    name = models.CharField(max_length=25)
    type = models.CharField(max_length=10)
    project = models.ForeignKey(
        MusicTrackProject, models.CASCADE, 'instruments'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(MusicInstrumentSetting, 'instrument', *args, **kwargs)


class MusicInstrumentEffect(ModelWithSettings):
    '''
    Модель эффекта музыкального инструмента

    :param type: тип эффекта (из библиотеки Tone.js)
    :param instrument: инструмент
    '''

    type = models.CharField(max_length=25)
    instrument = models.ForeignKey(
        MusicInstrument, models.CASCADE, 'effects'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(MusicInstrumentEffectSetting, 'effect', *args, **kwargs)


class MusicInstrumentSetting(JSONSetting):
    '''
    Модель настройки музыкального инструмента

    :param instrument: инструмент
    '''

    instrument = models.ForeignKey(
        MusicInstrument, models.CASCADE, 'settings'
    )


class MusicInstrumentEffectSetting(JSONSetting):
    '''
    Модель настройки эффекта музыкального инструмента

    :param effect: эффект инструмента
    '''

    effect = models.ForeignKey(
        MusicInstrumentEffect, models.CASCADE, 'settings'
    )


class MusicTrackPattern(models.Model):
    '''
    Модель паттерна проекта

    :param name: имя паттерна
    :param color: цвет паттерна в редакторе
    :param duration: продолжительность
    '''

    project = models.ForeignKey(MusicTrackProject, models.CASCADE, 'patterns')
    name = models.CharField(max_length=25)
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

    pattern = models.ForeignKey(MusicTrackPattern, models.CASCADE, 'notes')
    position = models.FloatField(validators=[MinValueValidator(0)])
    duration = models.FloatField(validators=[MinValueValidator(0.05)])
    notation = models.PositiveIntegerField(choices=NOTATION_CHOICES)
    octave = models.PositiveIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(7)]
    )
