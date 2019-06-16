from django.core.validators import RegexValidator
from django.forms import ModelForm, Textarea, CharField

from patients.Models import Patient


class PatientForm(ModelForm):
    # name = CharField(validators=[RegexValidator('^')])

    class Meta:
        model = Patient
        fields = ['name', 'gender', 'birth_date', 'email', 'phone', 'RG', 'CPF', 'comments', 'found_us_by', 'address']
        labels = {
             'name': 'Nome',
             'gender': 'Genêro',
             'birth_date': 'Data de Nascimento',
             'email': 'E-mail',
             'phone': 'Telefone',
             'RG': 'Identidade (RG)',
             'comments': 'Observações',
             'found_us_by': 'Como Nos Encontrou',
             'address': 'Endereço'
        }
        widgets = {
             'comments': Textarea(attrs={'rows':5}),
             'found_us_by': Textarea(attrs={'rows':5})
        }
