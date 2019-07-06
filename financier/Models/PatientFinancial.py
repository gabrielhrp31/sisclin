from django.db import models
from patients.Models.Patient import Patient
from consultations.Models.Consultation import Consultation
import datetime

class PatientFinancial(models.Model):
    # data, hora, descricao, valor total, valor pago,
    # saldo devedor, forma de pagamento, parcelas, 
    # data de pagamento, status
    description = models.TextField(null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET(None), null=True, verbose_name='Paciente')
    consultation = models.ForeignKey(Consultation, on_delete=models.SET(None), null=True, verbose_name='Consulta')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=7, decimal_places=2)
    payment_form = models.NullBooleanField(null=False)
    plots = models.IntegerField(null=True)
    payday = models.DateField(null=True)
    creation_date = models.DateField(auto_now_add=True)
    change_date = models.DateField(null=False)
    change_hour = models.TimeField(null=True)
    status = models.NullBooleanField(null=False)
    
    def __str__(self):
        return self.patient.id+' - '+self.consultation.id+' - '+self.description+' - '+self.amount+' - '+self.status

    def get_payment_form(self):
        if(self.payment_form):
            return 'À vista'
        return 'À prazo'
    
    def get_status(self):
        if(self.status):
            return 'FINALIZADO'
        return 'PENDENTE'

    def get_outstanding_balance(self):
        return self.amount - self.amount_paid

    # def get_hour(self):
    #     return datetime.datetime.now().strftime('%H:%M:%S')

    def get_date(self):
        return datetime.date.today()

    def as_dict(self):
        return {
            'description', self.description,
            'patient', self.patient.id,
            'consultation', self.consultation.id,
            'amount', self.amount,
            'amount_paid', self.amount_paid,
            'outstanding_balance', self.get_outstanding_balance(),
            'payment_form', self.get_payment_form(),
            'plots', self.plots,
            'payday', self.payday,
            'creation_date', self.get_date(),
            'change_date', self.change_date,
            'change_hour', self.change_hour,
            'status', self.get_status(),
        }
