from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Node

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['title', 'slug', 'label', 'level', 'round_per_minute', 'power', 'mcc']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'round_per_minute': forms.TextInput(attrs={'class': 'form-input'}),
            'power': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {'title': 'НАЗВА ', 
                  'slug': 'НОМЕР', 
                  'label': 'ФОТО ',
                  'level': 'РІВЕНЬ',
                  'round_per_minute': 'ОБЕРТІВ / ХВ ',
                  'power': 'ПОТУЖНІСТЬ',
                  'mcc': 'МСС  ',}


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
