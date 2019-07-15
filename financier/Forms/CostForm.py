from django.core.validators import RegexValidator
from django.forms import ModelForm, Textarea, CharField, ChoiceField, Select,HiddenInput, DateInput, DateField, HiddenInput
from localflavor.br.forms import BRCPFField
from financier.Models.Cost import Cost
import datetime
from odonto import settings

BOOL_STATUS = ((True, 'FINALIZADO'), (False, 'PENDENTE'))
BOOL_PAYMENT = ((True, 'À vista'), (False, 'À prazo'))
BOOL_COST = ((True, 'Fixo'), (False, 'Variável'))


class CostForm(ModelForm):
    # name = CharField(validators=[RegexValidator('^')])
    cost_type = ChoiceField(choices=BOOL_COST, label="Custo",
                            initial='', widget=Select(), required=True)
    description = CharField(label='Descrição')
    amount = CharField(label='Valor total', initial='0.00')
    payment_form = ChoiceField(choices=BOOL_PAYMENT, label="Forma de pagamento",
                         initial='True', widget=Select(), required=True)
    num_plots = CharField(label='Número de parcelas', widget=Textarea(attrs={'rows': 1, 'style': 'display:none;'}), initial='1', disabled=False)
    payday = DateField(label='Data de vencimento')
    # payday = DateField(label='Data de vencimento', 
    #                     widget=DateInput(format='%d/%m/%Y', 
    #                                     attrs={'class': "input", 'placeholder': "Ex.: dd/mm/aaaa", "OnKeyPress":"mask('##/##/####', this)"}))
    status = ChoiceField(choices=BOOL_STATUS, label="Situação",
                         initial='', widget=Select(), required=True)

    class Meta:
        model = Cost
        fields = '__all__'
        exclude = ['creation_date', 'change_hour', 'plots']
