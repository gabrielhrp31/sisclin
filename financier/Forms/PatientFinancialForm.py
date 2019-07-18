from django.core.validators import RegexValidator
from django.forms import ModelForm, Textarea, CharField, ChoiceField, Select,HiddenInput, DateInput, DateField, HiddenInput
from localflavor.br.forms import BRCPFField
from financier.models import PatientFinancial
import datetime
from odonto import settings

BOOL_STATUS = ((True, 'FINALIZADO'), (False, 'PENDENTE'))
BOOL_PAYMENT = ((True, 'À vista'), (False, 'À prazo'))


class PatientFinancialForm(ModelForm):
    # name = CharField(validators=[RegexValidator('^')])
    
    description = CharField(label='Descrição')
    amount = CharField(label='Valor total', required=True)
    amount_paid = CharField(label='Entrada', required=True)
    payment_form = ChoiceField(choices=BOOL_PAYMENT, label="Forma de pagamento",
                         initial='True', widget=Select(), required=True)
    num_plots = CharField(label='Número de parcelas', widget=Textarea(attrs={'rows': 1, 'style': 'display:none;'}), initial='1', disabled=False)
    payday = DateField(label='Data de vencimento', widget=DateInput(format='%d/%m/%Y'))
    status = ChoiceField(choices=BOOL_STATUS, label="Situação",
                         initial='', widget=Select(), required=True)

    class Meta:
        model = PatientFinancial
        fields = '__all__'
        exclude = ['creation_date', 'change_hour', 'consultation', 'plots']
