from django.forms import ModelForm, CharField, Textarea
from patients.Models.Address import Address
from localflavor.br.forms import BRStateChoiceField, BRZipCodeField


class AddressForm(ModelForm):
    # country = BRStateChoiceField(label="Estado")
    # postal_code = BRZipCodeField(label="CEP")

    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'city': 'Cidade',
            'postal_code': 'CEP',
            'street': 'Rua',
            'number': 'Número'
        }
        widgets = {
             'country': Textarea(attrs={'rows': 1, 'style': 'r  esize:none'}),
             'city': Textarea(attrs={'rows': 1, 'style': 'resize:none'}),
             'postal_code': Textarea(attrs={'rows': 1, 'style': 'resize:none'}),
             'street': Textarea(attrs={'rows': 1, 'style': 'resize:none'}),
        }
