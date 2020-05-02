from django.forms import ModelForm, FloatField, NumberInput, ChoiceField, Select
from ..models.settings import ModelWithSettings, SettingValue, FloatSettingValue, ChoiceSettingValue
from ..utils import zip_dict


class SettingsModelForm(ModelForm):

    class Meta:
        model = ModelWithSettings
        fields = []

    @staticmethod
    def make_float_field(sname: str, setting: FloatSettingValue):
        return FloatField(
            max_value=setting.max,
            min_value=setting.min,
            label=sname,
            widget=NumberInput(attrs={
                'class': 'form-control',
                'step': setting.step,
            })
        )

    @staticmethod
    def make_choice_field(sname: str, setting: ChoiceSettingValue):
        return ChoiceField(
            label=sname,
            choices=list(zip(setting.choices, setting.choices)),
            widget=Select(attrs={
                'class': 'form-control'
            })
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = self.instance.get_all_settings()
        definition = self.instance.definition

        self.field_makers_map = {
            'float': self.make_float_field,
            'choice': self.make_choice_field
        }

        self.field_order = ['.volume']
        self.generate_fields(zip_dict(definition, settings))

    def generate_fields(self, settings, path='', group='.'):
        for sname, d, v in settings:
            path += '.' + sname
            if isinstance(v, dict):
                self.generate_fields(zip_dict(d, v), path, sname)
            elif not isinstance(d, SettingValue):
                raise ValueError(f'invalid definition value: {d}')
            else:
                make_f = self.field_makers_map.get(d.type, None)
                if make_f is None:
                    raise ValueError(f'unsupported setting value {d.type}')

                field = make_f(sname, d)
                field.group = group
                self.fields[path] = field
                self.initial[path] = v
                self.field_order.append(path)
