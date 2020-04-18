from django.forms import Form, CharField, TextInput, Select
from ..models import MusicInstrument


class CreateMusicInstrumentForm(Form):
    '''
    Форма создания музыкального инструмента
    '''

    name = CharField(
        label='Имя',
        max_length=25,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя нового музыкального инструмента'
        })
    )

    type = CharField(
        label='Тип инструмента',
        max_length=15,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(type, type) for type in MusicInstrument.DEFINITIONS]
        self.fields['type'].widget = Select(
            choices=choices,
            attrs={
                'class': 'form-control'
            }
        )
