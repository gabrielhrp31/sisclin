from django.core.validators import RegexValidator
from django.forms import ModelForm, Textarea, CharField, ChoiceField, Select,HiddenInput, DateInput, DateField
from localflavor.br.forms import BRCPFField
from financier.models import PatientFinancial
import datetime
from odonto import settings

BOOL_STATUS = ((True, 'FINALIZADO'), (False, 'PENDENTE'))
BOOL_PAYMENT = ((True, 'À vista'), (False, 'À prazo'))


class PatientFinancialForm(ModelForm):
    # name = CharField(validators=[RegexValidator('^')])
    
    description = CharField(label='Descrição')
    amount = CharField(label='Valor total', initial='0.00')
    amount_paid = CharField(label='Valor pago', initial='0.00')
    outstanding_balance = CharField(label='Saldo devedor', initial='0.00', disabled=True)
    payment_form = ChoiceField(choices=BOOL_PAYMENT, label="Forma de pagamento",
                         initial='', widget=Select(), required=True)
    plots = CharField(label='Número de parcelas', initial='0')
    payday = DateField(label='Data de vencimento', 
                        widget=DateInput(format='%d/%m/%Y', 
                                        attrs={'class': "input", 'placeholder': "Ex.: dd/mm/aaaa", "OnKeyPress":"mask('##/##/####', this)"}))
    # hour = CharField(label='Hora de registro')
    # date = CharField(label='Data de registro')
    # creation_date = datetime.date.today()
    change_date = datetime.date.today()
    change_hour = datetime.datetime.now().strftime('%H:%M:%S')
    # date = datetime.datetime.now().strftime('%Y-%B-%d')
    status = ChoiceField(choices=BOOL_STATUS, label="Situação",
                         initial='', widget=Select(), required=True)

    class Meta:
        model = PatientFinancial
        fields = '__all__'
        exclude = ['change_date', 'change_hour']