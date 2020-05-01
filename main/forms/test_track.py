from django import forms


class CreateTestTrack(forms.Form):
    '''
    Форма создания пробного трека

    :param name: поле имяни трека
    :param desc: поле описания трека
    :param allow_comments: разрешены ли комментарии
    :param allow_rating: разрешены ли лайки / дизлайки
    :param allow_reusing: разрешено ли свободное использование
    '''

    name = forms.CharField(
        max_length=150,
        required=True,
        label='Имя трека',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя трека',
            }
        )
    )

    desc = forms.CharField(
        max_length=250,
        required=True,
        label='Описание трека',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Описание трека',
            }
        )
    )

    allow_rating = forms.BooleanField(
        required=False,
        label='Доступ к лайкам',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    allow_reusing = forms.BooleanField(
        required=False,
        label='Доступ к свободному использованию',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    allow_comments = forms.BooleanField(
        required=False,
        label='Доступ к комментированию',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            }
        )
    )