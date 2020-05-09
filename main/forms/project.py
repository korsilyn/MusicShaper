'''
Модуль формы редактирования проекта (имя, описание)
'''

from datetime import datetime
from django.forms import ModelForm, TextInput, Textarea
from ..models import MusicTrackProject, TrackProjectSettings


class ProjectForm(ModelForm):
    '''
    Форма создания проекта
    '''

    class Meta:
        model = MusicTrackProject
        fields = ['name', 'desc']
        labels = {
            'name': 'Имя',
            'desc': 'Описание'
        }
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Имя нового проекта',
                'class': 'form-control'
            }),
            'desc': Textarea(attrs={
                'placeholder': 'Описание нового проекта',
                'class': 'form-control',
                'style': 'min-height: 40px; height: 80px'
            })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['desc'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.user
        instance.creation_date = datetime.now()
        instance.save()
        if not hasattr(instance, 'settings'):
            TrackProjectSettings.objects.create(
                project=instance,
                bpm=120,
            )
        return instance
