'''
===============================================
Модуль формы создания / редактирования паттерна
===============================================
'''

from django.forms import ModelForm, TextInput, NumberInput, Select
from django.db.models import F
from ..models import MusicTrackPattern, MusicNote


class TrackPatternForm(ModelForm):
    '''
    **Форма создания / редактирования паттерна**
    '''

    class Meta:
        model = MusicTrackPattern
        fields = ('name', 'duration', 'color')
        labels = {
            'name': 'Имя',
            'duration': 'Продолжительность (количество строк)',
            'color': 'Цвет в редакторе',
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
            }),
            'color': Select(attrs={
                'class': 'form-control',
                'onchange': 'this.style.borderColor = this.value',
            }),
        }

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.fields['duration'].widget.attrs['min'] = 10

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.project = self.project
        instance.save()
        MusicNote.objects.filter(pattern=instance)\
            .annotate(end_time=F('time') + F('length'))\
            .filter(end_time__gt=instance.duration)\
            .delete()
        return instance
