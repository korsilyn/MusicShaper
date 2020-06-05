'''
Модуль формы для управления треком
'''

from django.forms import ModelForm, BooleanField, IntegerField,\
    TextInput, Textarea, CheckboxInput, Select
from django.utils.translation import gettext
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
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Имя трека',
                'class': 'form-control',
            }),
            'desc': Textarea(attrs={
                'placeholder': 'Описание трека',
                'class': 'form-control',
                'style': 'min-height: 40px; height: 60px;',
            }),
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
        label='Доступ оценкам',
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

    def __init__(self, *, instance=None, **kwargs):
        super().__init__(instance=instance, **kwargs)
        access_chocies = self.fields['access'].widget.choices
        self.fields['access'].widget.choices = \
            list(map(lambda choice: (choice[0], gettext(choice[1])), access_chocies))
        if instance is not None:
            self.initial['access'] = instance.settings.access
            self.initial['allow_rating'] = instance.settings.allow_rating
            self.initial['allow_reusing'] = instance.settings.allow_reusing
            self.initial['allow_comments'] = instance.settings.allow_comments

    def save(self, commit=True):
        instance = super().save(commit=True)
        instance.settings.access = self.data['access']
        instance.settings.allow_comments = self.data.get('allow_comments', 'off') == 'on'
        instance.settings.allow_rating = self.data.get('allow_rating', 'off') == 'on'
        instance.settings.allow_reusing = self.data.get('allow_reusing', 'off') == 'on'
        instance.settings.save()
        return instance
