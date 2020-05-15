'''
Модуль абстрактной модели ModelWithSettings

Модель нужна для эффективного хранения различных настроект
моделей в базе данных

От этой модели наследуются музыкальные инструменты и эффекты
'''

from math import inf
from abc import ABC, abstractmethod
from django.db import models
from jsonfield import JSONField


class SettingValue(ABC):
    '''
    Абстрактный класс поля настройки объекта
    '''

    def __init__(self, *, _type, initial, **values):
        self.type = _type
        self.initial = initial
        for key, value in values.items():
            setattr(self, key, value)

    @abstractmethod
    def validate_value(self, value) -> bool:
        '''
        Абстрактный метод, проверяющий значение `value`

        :param value: значение для проверки
        '''


class FloatSettingValue(SettingValue):
    '''
    Числовое (float) поле настройки объекта
    '''

    def __init__(self, *, initial, min_v=-inf, max_v=inf, step=0.1):
        super().__init__(
            _type='float',
            initial=float(initial),
            min=float(min_v),
            max=float(max_v),
            step=float(step),
        )

    def validate_value(self, value):
        return isinstance(value, (float, int)) and self.min <= value <= self.max


class IntSettingValue(SettingValue):
    '''
    Числовое (int) поле настройки объекта
    '''

    def __init__(self, *, initial, min_v=None, max_v=None):
        super().__init__(
            _type='int',
            initial=int(initial),
            min=int(min_v) if min_v is not None else None,
            max=int(max_v) if max_v is not None else None,
        )

    def validate_value(self, value):
        min_v = self.min if self.min is not None else -inf
        max_v = self.max if self.max is not None else inf
        return isinstance(value, int) and min_v <= value <= max_v


class ChoiceSettingValue(SettingValue):
    '''
    Поле настройки объекта с выбором значения
    '''

    def __init__(self, *, initial, choices):
        if initial not in choices:
            raise ValueError(f'initial \'{initial}\' not found in choices')
        super().__init__(
            _type='choice',
            initial=initial,
            choices=choices,
        )

    def validate_value(self, value):
        return value in self.choices


class ModelWithSettings(models.Model):
    '''
    Абстрактная модель *кхм* модели, у которой
    есть словарь настроек

    У класса дочерней модели также появляется метод
    `define`, с помощью которого можно задать стандартные
    настройки для определённого 'типа' объекта модели
    '''

    class Meta:
        abstract = True

    type = models.CharField(max_length=25)
    json_settings = JSONField()

    DEFINITIONS = dict()

    def __init_subclass__(cls):
        super().__init_subclass__()
        setattr(cls, 'DEFINITIONS', dict())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.assert_type(TypeError)
        except TypeError:
            self.reset()
            self.type = next(iter(self.DEFINITIONS.keys()))
            if hasattr(self, 'project'):
                self.save()

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

    def assert_type(self, error_class=TypeError):
        '''
        Кидает error_class в случае, если тип инструмента
        объявлен некорректно

        :param error_class: класс ошибки
        '''

        if self.type not in self.DEFINITIONS:
            raise error_class(f'type {self.type} is not defined')

    @property
    def definition(self):
        '''
        Сокращение для быстрого доступа к текущему
        объявлению настроек объекта
        '''

        return self.DEFINITIONS[self.type]

    def reset(self):
        '''
        Сбрасывает все текущие настройки инструмента
        '''

        self.json_settings.clear()

    def get_settings_recursive(self, definition, json_settings):
        '''
        Рекурсивно возвращает словарь настроек

        :param definition: текущий словарь объявления
        :param json_settings: текущий словарь с настройками
        '''

        for sname, vdef in definition.items():
            if isinstance(vdef, dict):
                value = json_settings.get(sname, dict())
                yield sname, dict(self.get_settings_recursive(vdef, value))
            elif not isinstance(vdef, SettingValue):
                raise ValueError(f'invalid setting definition {sname}')
            else:
                yield sname, json_settings.get(sname, vdef.initial)

    def get_settings_generator(self):
        '''
        Возвращает текущие настройки объекта (генератор)
        '''

        self.assert_type()
        yield from self.get_settings_recursive(self.definition, self.json_settings)

    def get_settings(self):
        '''
        Возвращает текущие настройки объекта
        '''
        return dict(self.get_settings_generator())
