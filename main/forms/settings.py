from django.forms import ModelForm, FloatField, NumberInput, ChoiceField, Select
from ..models.settings import ModelWithSettings, SettingValue, FloatSettingValue, ChoiceSettingValue


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

        settings = self.instance.get_settings()
        definition = self.instance.definition

        self.field_makers_map = {
            'float': self.make_float_field,
            'choice': self.make_choice_field
        }

        try:
            self.generate_fields(definition, settings)
        except KeyError:
            raise ValueError('invalid instrument type')

    def grouped_fields(self):
        groups = dict()
        visible_fields = self.visible_fields()
        for bound in visible_fields:
            groups.setdefault(bound.field.group, []).append(bound)
        return groups

    def generate_fields(self, definition, settings, path=''):
        ipath = path
        for sname, d in definition.items():
            v = settings[sname]
            path = ipath + '.' + sname
            if isinstance(v, dict):
                self.generate_fields(d, v, path)
            elif not isinstance(d, SettingValue):
                raise ValueError(f'invalid definition value: {d}')
            else:
                make_f = self.field_makers_map.get(d.type, None)
                if make_f is None:
                    raise ValueError(f'unsupported setting value {d.type}')

                field = make_f(sname, d)
                field.required = False
                group = path.split('.')[-2] or '.'
                field.group = group
                self.fields[path] = field
                self.initial[path] = v

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        definition = instance.definition

        for path, value in self.data.items():
            if not path.startswith('.'):
                continue

            try:
                value = float(value)
            except ValueError:
                pass

            keys = path[1:].split('.')
            d_dict = definition
            for key in keys[:-1]:
                d_dict = d_dict.get(key, None)
                if not isinstance(d_dict, dict):
                    raise ValueError(f'invalid setting update path {path}')

            vdef = d_dict.get(keys[-1], None)
            if not isinstance(vdef, SettingValue):
                raise ValueError(f'invalid setting update path {path}')

            if value != vdef.initial:
                if not vdef.validate_value(value):
                    raise ValueError(f'invalid setting value {value} ({type(value)}) for {path}')

                s_dict = instance.json_settings
                for key in keys[:-1]:
                    s_dict = s_dict.setdefault(key, dict())
                s_dict[keys[-1]] = value

        instance.save(*args, **kwargs)
        return instance
