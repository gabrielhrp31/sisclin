from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class UpdateProfile(ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = (
            {
                'first_name': 'Nome',
                'last_name': 'Sobrenome'
            }
        )