from django.forms import ModelForm, CharField, TextInput, Textarea
from ..models import MusicTrackProject


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desc'].required = False
