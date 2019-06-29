from django.core.validators import RegexValidator
from django.forms import ModelForm, Textarea, CharField, ChoiceField, Select,HiddenInput
from localflavor.br.forms import BRCPFField
from patients.models import Patient

BOOL_CHOICES = ((True, 'Masculino'), (False, 'Feminino'))


class PatientForm(ModelForm):
    # name = CharField(validators=[RegexValidator('^')])
    gender = ChoiceField(choices=BOOL_CHOICES, label="Genêro",
                         initial='', widget=Select(), required=True)
    name = CharField(label='Nome')
    birth_date = CharField(label='Data de Nascimento')
    phone = CharField(label='')
    CPF = BRCPFField(label="CPF")
    RG = CharField(label='RG (Identidade)')
    comments = CharField(label='Observações')
    found_us_by = CharField(label='Como nos Encontrou')
    

    class Meta:
        model = Patient
        # fields = ['name', 'gender', 'birth_date', 'email', 'phone', 'RG', 'CPF', 'comments', 'found_us_by', 'address']
        # id = id_address name=id_address
        fields = '__all__'
        widgets = {
            'address': HiddenInput()
        }