from django.forms import ModelForm, CharField, Textarea
from patients.Models.Address import Address
from localflavor.br.forms import BRStateChoiceField, BRZipCodeField


class AddressForm(ModelForm):
    country = BRStateChoiceField(label="Estado")
    city = CharField(label="Cidade")
    street = CharField(label="Rua")
    district = CharField(label="Complemento/Bairro")
    
    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'number': 'Número'
        }