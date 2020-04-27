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


class BaseSettingValue(ABC):
    @abstractmethod
    def match_json(self, value: tuple) -> bool:
        '''
        Если возвращает True, то класс понимает value
        как нечтно, что он может спокойно прочитать
        '''

    @abstractmethod
    def get_value_from_json(self):
        '''
        Получает значение настройки из её json формата
        громкость: (0, -10, 5) -> 0
        '''


class NumberSetting(BaseSettingValue):
    def match_json(self, *json_setting: tuple):
        return all(isinstance(v, (int, float)) for v in json_setting) and 0 < len(json_setting) <= 4

    def get_value_from_json(self, value, min=-inf, max=inf, step=0.1):
        min = float(min)
        max = float(max)
        value = float(value)
        return (value if value <= max else max) if value >= min else min


class ChoiceSetting(BaseSettingValue):
    def match_json(self, *json_setting: tuple):
        return all(isinstance(v, str) for v in json_setting)

    def get_value_from_json(self, *choices):
        return choices[0]


class ModelWithSettings(models.Model):
    '''
    Абстрактная модель *кхм* модели, у которой
    есть список настроек (JSONSetting)

    У класса дочерней модели также появляется метод
    define, с помощью которого можно задать стандартные
    настройки для определённого 'типа' объекта модели
    '''

    SETTING_JSON_PARSERS: List[BaseSettingValue] = [
        NumberSetting(), ChoiceSetting()
    ]

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
            **{self.settingRelatedName: self}).delete()

    def get_setting_value(self, json_setting, default=None):
        '''
        Превращает значение настройки из 'формата define'
        в простое значение

        пример:
        { 'value': (0.5, 0, 1) }
        после функции станет
        { 'value': 0.5 }
        '''

        if not (isinstance(json_setting, tuple) and len(json_setting) >= 2):
            return default

        for p in self.SETTING_JSON_PARSERS:
            if p.match_json(*json_setting):
                return p.get_value_from_json(*json_setting)

        return default

    def clean_setting_dict(self, setting: dict) -> dict:
        '''
        Превращает словарь настроек из 'формата define'
        в словарь, содержащий только значения

        пример:
        { 's': { 'value': (0.5, 0, 1) } }
        после функции станет
        { 's': { 'value': 0.5 } }
        '''

        rs = {}
        for key, value in setting.items():
            if isinstance(value, dict):
                rs[key] = self.clean_setting_dict(value)
            else:
                rs[key] = self.get_setting_value(value)
        return rs

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

    def get_setting_model(self, name: str, assert_type=True):
        if assert_type:
            self.assert_type()
        return self.settingModel.objects.get_or_create(
            **{self.settingRelatedName: self},
            name=name
        )

    def get_all_settings(self) -> dict:
        '''
        Возвращает словарь текущих настроек инструмента

        :rtype: dict
        '''

        self.assert_type()
        return self.clean_setting_dict({
            sname: self.get_setting(sname, False) for sname in self.definition
        })
