from django.core.validators import RegexValidator
from django.forms import ModelForm, Textarea, CharField, ChoiceField, Select

from patients.models import Patient

BOOL_CHOICES = ((True, 'Masculino'), (False, 'Feminino'))


class PatientForm(ModelForm):
    # name = CharField(validators=[RegexValidator('^')])
    gender = ChoiceField(choices=BOOL_CHOICES, label="Genêro",
                              initial='', widget=Select(), required=True)

    class Meta:
        model = Patient
        # fields = ['name', 'gender', 'birth_date', 'email', 'phone', 'RG', 'CPF', 'comments', 'found_us_by', 'address']
        # id = id_address name=id_address
        exclude = ['address']
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
             'comments': Textarea(attrs={'rows': 5, 'style': 'resize:none'}),
             'found_us_by': Textarea(attrs={'rows': 5, 'style': 'resize:none'}),
             'RG': Textarea(attrs={'rows': 1, 'style': 'resize:none'}),
             'phone': Textarea(attrs={'rows': 1, 'style': 'resize:none'}),
             'name': Textarea(attrs={'rows': 1, 'style': 'resize:none'}),
             'CPF': Textarea(attrs={'rows': 1, 'style': 'resize:none'}),
        }
