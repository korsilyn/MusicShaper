from django.db import models
from abc import ABC, abstractmethod
from jsonfield import JSONField
from typing import List
from math import inf


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


class SettingValue:
    def __init__(self, *, type, initial, **values):
        self.type = type
        self.initial = initial
        for k, v in values.items():
            setattr(self, k, v)


class FloatSettingValue(SettingValue):
    def __init__(self, *, initial, min=-inf, max=inf, step=0.1):
        super().__init__(
            type='float',
            initial=float(initial),
            min=float(min),
            max=float(max),
            step=float(step),
        )


class ChoiceSettingValue(SettingValue):
    def __init__(self, *, initial, choices):
        if initial not in choices:
            raise ValueError(f'initial \'{initial}\' not found in choices')
        super().__init__(
            type='choice',
            initial=initial,
            choices=choices,
        )


class ModelWithSettings(models.Model):
    '''
    Абстрактная модель *кхм* модели, у которой
    есть список настроек (`JSONSetting`)

    У класса дочерней модели также появляется метод
    `define`, с помощью которого можно задать стандартные
    настройки для определённого 'типа' объекта модели
    '''

    class Meta:
        abstract = True

    def __init_subclass__(cls):
        super().__init_subclass__()
        setattr(cls, 'DEFINITIONS', dict())

    def __init__(self, settingModel, related_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settingModel = settingModel
        self.settingRelatedName = related_name

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

    def assert_type(self, error_class=NameError):
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

        self.settingModel.objects.filter(
            **{self.settingRelatedName: self}
        ).delete()

    def get_setting(self, name: str, assert_type=True) -> dict:
        '''
        Возвращает настройку объекта в виде словаря

        :param name: имя настройки
        :param assert_type: проверять ли тип объекта
        '''

        if assert_type:
            self.assert_type()
        try:
            return self.settingModel.objects.get(**{self.settingRelatedName: self}, name=name).data
        except self.settingModel.DoesNotExist:
            return self.definition[name]

    def clean_setting_dict(self, setting: dict) -> dict:
        rs = {}
        for key, value in setting.items():
            if isinstance(value, dict):
                rs[key] = self.clean_setting_dict(value)
            elif isinstance(value, SettingValue):
                rs[key] = value.initial
            else:
                rs[key] = value
        return rs

    def get_all_settings(self) -> dict:
        '''
        Возвращает словарь текущих настроек инструмента

        :rtype: dict
        '''

        self.assert_type()
        return self.clean_setting_dict({
            sname: self.get_setting(sname, False) for sname in self.definition
        })
