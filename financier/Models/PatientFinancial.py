from django.db import models
from patients.Models.Patient import Patient
from consultations.Models.Consultation import Consultation
import datetime


class PatientFinancial(models.Model):
    # data, hora, descricao, valor total, valor pago,
    # saldo devedor, forma de pagamento, parcelas, 
    # data de pagamento, status
    description = models.TextField(null=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, null=True, verbose_name='Consulta')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    payment_form = models.NullBooleanField(null=False)
    num_plots = models.IntegerField(default='1')
    payday = models.DateField(null=False, default=datetime.date.today)
    creation_date = models.DateField(auto_now_add=True)
    change_date = models.DateField(null=False, auto_now=True)
    change_hour = models.TimeField(null=False, auto_now=True)

    def get_payment_form(self):
        return 'À vista' if self.payment_form else 'À prazo'

    def get_outstanding_balance(self):
        return self.amount - self.amount_paid

    # def get_hour(self):
    #     return datetime.datetime.now().strftime('%H:%M:%S')

    def get_date(self):
        return datetime.date.today()

    def as_dict(self):
        return {
            'description', self.description,
            'consultation_id', self.consultation,
            'amount', self.amount,
            'amount_paid', self.amount_paid,
            'payment_form', self.payment_form,
            'num_plots', self.num_plots,
            'payday', self.payday,
            'creation_date', self.creation_date,
            'change_date', self.change_date,
            'change_hour', self.change_hour,
        }
