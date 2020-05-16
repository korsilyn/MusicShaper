'''
Модуль формы создания / редактирования паттерна
'''

from django.forms import ModelForm, TextInput, NumberInput
from ..models import MusicTrackPattern


class MusicPatternForm(ModelForm):
    '''
    Форма создания / редактирования паттерна
    '''

    class Meta:
        model = MusicTrackPattern
        fields = ('name', 'duration')
        labels = {
            'name': 'Имя',
            'duration': 'Продолжительность (количество строк)'
        }
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя паттерна'
            }),
            'duration': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Продолжительность паттерна',
                'max': 256
            })
        }

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.fields['duration'].widget.attrs['min'] = 10

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.project = self.project
        if commit:
            instance.save()
        return instance
