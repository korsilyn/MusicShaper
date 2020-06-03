'''
Модуль формы жалобы
'''

from django import forms


class ClaimForm(forms.Form):
    '''
    Форма жалобы на трек

    :param topic: тема жалобы
    :param content: содержание
    '''

    topic = forms.CharField(
        label='Тема',
        max_length=50,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Тема жалобы',
            }
        )
    )

    content = forms.CharField(
        label='Содержание',
        max_length=256,
        min_length=10,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Содержание жалобы',
            }
        )
    )
