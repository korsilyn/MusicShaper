'''
========================================
Модуль форм для музыкальных инструментов
========================================
'''

from django.forms import ModelForm, TextInput, Select
from ..models import MusicInstrument


class MusicInstrumentForm(ModelForm):
    '''
    **Форма создания / редактирования музыкального инструмента**
    '''

    class Meta:
        model = MusicInstrument
        fields = ('name', 'type', 'notesColor')

        labels = {
            'name': 'Имя',
            'type': 'Тип',
            'notesColor': 'Цвет музыкальных нот в редакторе',
        }

        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Имя инструмента',
                'class': 'form-control'
            }),
            'type': Select(attrs={
                'class': 'form-control'
            }),
            'notesColor': Select(attrs={
                'class': 'form-control',
                'onchange': 'this.style.borderColor = this.value',
            }),
        }

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(type, type) for type in MusicInstrument.DEFINITIONS]
        self.fields['type'].widget.choices = choices
        self.project = project

    def save(self, commit=True):
        instrument = super().save(commit=False)
        instrument.project = self.project
        if instrument.pk and 'type' in self.changed_data:
            instrument.reset()
        if commit:
            instrument.save()
        return instrument
