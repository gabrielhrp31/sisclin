from django.forms import ModelForm, CharField

from consultations.Models.Procedure import Procedure


class ProcedureForm(ModelForm):
    name = CharField(label="Nome do Procedimento")

    class Meta:
        model = Procedure
        fields = '__all__'
        labels = {
            'price': 'Preço Padrão'
        }
