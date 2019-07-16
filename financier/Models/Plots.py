from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal

from financier.models import PatientFinancial


class Plots(models.Model):
    patient_financial = models.ForeignKey(PatientFinancial, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date = models.DateField(null=True)
    paid_day = models.DateField(null=True)
    # se esse for verdadeiro é uma entrada
    input = models.BooleanField(null=False, default=False)

    def create(self, plot_price, plot_date, patient_financier, input=False):
        self.price = plot_price
        self.date = plot_date
        self.patient_financial = patient_financier
        self.input = input
        self.save()

    def get_type(self):
        if self.input:
            return '<span class="label label-default">Entrada</span>'
        return '<span class="label label-default">Parcela</span>'

    def get_situation(self):
        if self.paid_day:
            return '<span class="label label-success">Pago</span>'
        else:
            if self.date < datetime.now().date():
                return '<span class="label label-danger">Em Atraso</span>'
            return '<span class="label label-info">Em aberto</span>'

    def pay(self, date):
        self.paid_day = date
        self.save()