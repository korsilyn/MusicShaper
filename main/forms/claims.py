from django import forms


class ClaimForm(forms.Form):
    topic = forms.CharField(
        label='',
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
        label='',
        max_length=256,
        min_length=10,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Содержание жалобы',
            }
        )
    )
