from django.forms import ModelForm, CharField, Textarea
from patients.Models.Address import Address
from localflavor.br.forms import BRStateChoiceField, BRZipCodeField


class AddressForm(ModelForm):
    postal_code = CharField(label="CEP")
    country = BRStateChoiceField(label="Estado", disabled=True)
    city = CharField(label="Cidade", widget=Textarea(attrs={'rows': 1, 'style': 'resize:none;', 'disabled': True}))
    street = CharField(label="Rua")
    district = CharField(label="Complemento/Bairro")
    
    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'number': 'Número'
        }