from django.core.validators import RegexValidator
from django.forms import ModelForm, Textarea, CharField, ChoiceField, Select,HiddenInput
from localflavor.br.forms import BRCPFField
from patients.models import PatientFinancial

BOOL_STATUS = ((True, 'FINALIZADO'), (False, 'PENDENTE'))
BOOL_PAYMENT = ((True, 'À vista'), (False, 'À prazo'))


class PatientFinancialForm(ModelForm):
    # name = CharField(validators=[RegexValidator('^')])
    
    date = CharField(label='Data de registro')
    hour = CharField(label='Hora de registro')
    description = CharField(label='Descrição')
    amount = CharField(label='Valor total')
    amount_paid = CharField(label='Valor pago')
    outstanding_balance = CharField(label='Saldo devedor')
    payment_form = ChoiceField(choices=BOOL_PAYMENT, label="Forma de pagamento",
                         initial='', widget=Select(), required=True)
    plots = CharField(label='Número de parcelas')
    payday = CharField(label='Dia do vencimento')
    status = ChoiceField(choices=BOOL_STATUS, label="Situação",
                         initial='', widget=Select(), required=True)

    class Meta:
        model = PatientFinancial
        # fields = ['name', 'gender', 'birth_date', 'email', 'phone', 'RG', 'CPF', 'comments', 'found_us_by', 'address']
        # id = id_address name=id_address
        fields = '__all__'