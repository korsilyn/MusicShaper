from django.forms import ModelForm, TextInput, Select
from ..models import MusicInstrument


class MusicInstrumentForm(ModelForm):
    '''
    Форма создания / редактирования музыкального инструмента
    '''

    class Meta:
        model = MusicInstrument
        fields = ('name', 'type')

        labels = {
            'name': 'Имя',
            'type': 'Тип'
        }

        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Имя инструмента',
                'class': 'form-control'
            }),
            'type': Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(type, type) for type in MusicInstrument.DEFINITIONS]
        self.fields['type'].widget.choices = choices

    def save(self, *args, **kwargs):
        instrument = super().save(commit=False)
        if instrument.pk and 'type' in self.changed_data:
            instrument.reset()
        instrument.save(*args, **kwargs)
        return instrument
