from django.db import models
from financier.Models.PatientFinancial import PatientFinancial


class CashFlow(models.Model):
    # data, hora, descricao, valor total, valor pago,
    # saldo devedor, forma de pagamento, parcelas, 
    # data de pagamento, status
    entrada = patient_id = models.ForeignKey(PatientFinancial, on_delete=models.SET(None), null=True)
    saida = patient_id = models.ForeignKey(PatientFinancial, on_delete=models.SET(None), null=True)
    date = models.DateField(null=False)
    hour = models.TimeField(null=True)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=7, decimal_places=2)
    payment_form = models.NullBooleanField(null=False)
    plots = models.IntegerField(null=True)
    payday = models.IntegerField(null=True)
    status = models.NullBooleanField(null=False)
    
    def __str__(self):
        return self.description+' - '+self.amount+' - '+self.status

    def as_dict(self):
        return {
            'date', self.date,
            'hour', self.hour,
            'description', self.description,
            'amount', self.amount,
            'amount_paid', self.amount_paid,
            'outstanding_balance', self.outstanding_balance,
            'payment_form', self.payment_form,
            'plots', self.plots,
            'payday', self.payday,
            'status', self.status,
        }
