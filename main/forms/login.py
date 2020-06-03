'''
========================
Модуль формы авторизации
========================
'''

from django import forms


class LoginForm(forms.Form):
    '''
    **Форма авторизации пользователя**

    :param username: поле имя пользователя
    :param password: поле пароля
    '''

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Логин',
            }
        )
    )
    password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
            }
        )
    )
