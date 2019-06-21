from django.forms import ModelForm, CharField, Textarea
from patients.Models.Address import Address
from localflavor.br.forms import BRStateChoiceField, BRZipCodeField


class AddressForm(ModelForm):
    country = BRStateChoiceField(label="Estado")
    postal_code = BRZipCodeField(label="CEP")
    city = CharField(label="Cidade")
    street = CharField(label="Rua")
    
    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'number': 'Número'
        }