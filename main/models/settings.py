from django.db import models
from abc import ABC, abstractmethod
from jsonfield import JSONField
from typing import Union
from math import inf


NumberType = Union[int, float]


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
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def to_json(self) -> tuple:
        pass


class NumberSetting(BaseSettingValue):
    def __init__(self, value: NumberType, min: NumberType = -inf, max: NumberType = inf, step: NumberType = 0.1):
        super().__init__((value if value <= max else max) if value >= min else min)
        self.min = min
        self.max = max
        self.step = step

    def to_json(self) -> tuple:
        return (self.value, self.min, self.max, self.step)


class ChoiceSetting(BaseSettingValue):
    def __init__(self, value, *choices):
        super().__init__(value)
        self.choices = choices + (value,) if value not in choices else choices

    def to_json(self) -> tuple:
        return (self.choices)


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

    def reset(self):
        '''
        Сбрасывает все текущие настройки инструмента
        '''

        self.settingModel.objects.filter(
            **{self.settingRelatedName: self}).delete()

    def get_setting_value(self, json_setting):
        '''
        Превращает значение настройки из 'формата define'
        в простое значение

        пример:
        { 'value': (0.5, 0, 1) }
        после функции станет
        { 'value': 0.5 }
        '''

        if len(json_setting) < 2:
            return None

        v = json_setting[0]
        if isinstance(v, str):
            return ChoiceSetting(*json_setting).value
        if isinstance(v, int) or isinstance(v, float):
            return NumberSetting(*json_setting).value
        return None

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

    def get_setting_lazy(self, name: str, assert_type=True) -> dict:
        if assert_type:
            self.assert_type()
        try:
            return self.settingModel.objects.get(**{self.settingRelatedName: self}, name=name).data
        except self.settingModel.DoesNotExist:
            return self.DEFINITIONS[self.type][name]

    def get_json_settings(self) -> dict:
        '''
        Возвращает словарь текущих настроек инструмента
        '''

        self.assert_type()
        rsettings = {}
        for sname in self.DEFINITIONS[self.type]:
            rsettings[sname] = self.get_setting_lazy(sname)
        return self.clean_setting_dict(rsettings)

    def get_setting_by_path(self, path: str, default):
        keys = path.split('.')
        if len(keys) == 0:
            return default

        settings = self.get_setting_lazy(keys[0])
        for key in keys[1:]:
            settings = settings.get(key, None)
            if settings is None:
                return default

        if isinstance(settings, dict):
            return default

        return settings
