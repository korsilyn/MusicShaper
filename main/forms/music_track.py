'''
Модуль формы для управления треком
'''

from django.forms import ModelForm, BooleanField, IntegerField,\
    CheckboxInput, Select
from ..models import MusicTrack, TrackSettings


class MusicTrackForm(ModelForm):
    '''
    Форма управления треком
    '''

    class Meta:
        model = MusicTrack
        fields = ('name', 'desc')
        labels = {
            'name': 'Имя',
            'desc': 'Описание',
        }

    access = IntegerField(
        label='Уровень доступа',
        widget=Select(
            attrs={
                'class': 'form-control'
            },
            choices=TrackSettings.ACCESS_CHOICES,
        )
    )

    allow_rating = BooleanField(
        required=False,
        label='Доступ к лайкам',
        widget=CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    allow_reusing = BooleanField(
        required=False,
        label='Доступ к свободному использованию',
        widget=CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    allow_comments = BooleanField(
        required=False,
        label='Доступ к комментированию',
        widget=CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )


    def save(self, commit=True):
        instance = super().save(commit=True)
        instance.settings.access = self.data['access']
        instance.settings.allow_comments = self.data['allow_comments']
        instance.settings.allow_rating = self.data['allow_rating']
        instance.settings.allow_reusing = self.data['allow_reusing']
        instance.settings.save()
        return instance
