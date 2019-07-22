from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class CreateUser(ModelForm):
    """
        A form that creates a user, with no privileges, from the given username and
        password.
        """
    error_messages = {
        'password_mismatch': ("As duas senhas não conferem!"),
    }
    password1 = forms.CharField(label=("Senha"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Confirmar Senha"),
                                widget=forms.PasswordInput,
                                help_text=("Insira a mesma senha"))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = (
            {
                'first_name': 'Nome',
                'last_name': 'Sobrenome',
            }
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(CreateUser, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user