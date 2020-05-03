from django.db import models
from abc import ABC, abstractmethod
from jsonfield import JSONField
from typing import List
from math import inf


class SettingValue(ABC):
    def __init__(self, *, type, initial, **values):
        self.type = type
        self.initial = initial
        for k, v in values.items():
            setattr(self, k, v)

    @abstractmethod
    def validate_value(self, value) -> bool:
        pass


class FloatSettingValue(SettingValue):
    def __init__(self, *, initial, min=-inf, max=inf, step=0.1):
        super().__init__(
            type='float',
            initial=float(initial),
            min=float(min),
            max=float(max),
            step=float(step),
        )

    def validate_value(self, value):
        return isinstance(value, (float, int)) and self.min <= value <= self.max


class ChoiceSettingValue(SettingValue):
    def __init__(self, *, initial, choices):
        if initial not in choices:
            raise ValueError(f'initial \'{initial}\' not found in choices')
        super().__init__(
            type='choice',
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
        return self.DEFINITIONS[self.type]

    def reset(self):
        '''
        Сбрасывает все текущие настройки инструмента
        '''

        self.json_settings.clear()

    def get_settings_recursive(self, definition, json_settings):
        for sname, vdef in definition.items():
            if isinstance(vdef, dict):
                yield sname, dict(self.get_settings_recursive(vdef, json_settings.get(sname, dict())))
            elif not isinstance(vdef, SettingValue):
                raise ValueError(f'invalid setting definition {sname}')
            else:
                yield sname, json_settings.get(sname, vdef.initial)

    def get_settings_generator(self):
        self.assert_type()
        yield from self.get_settings_recursive(self.definition, self.json_settings)

    def get_settings(self):
        return dict(self.get_settings_generator())
