from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal

from financier.models import PatientFinancial
from financier.Models.Cost import Cost


class Plots(models.Model):
    patient_financial = models.ForeignKey(PatientFinancial, null=True, blank=True, on_delete=models.CASCADE)
    cost = models.ForeignKey(Cost, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date = models.DateField(null=True)
    paid_day = models.DateField(null=True)
    # True =  entrada e False=Parcela
    input = models.BooleanField(null=False, default=True)
    # 1 = entrada, 2 = saida
    type = models.IntegerField(null=False, default=2)

    def create(self, plot_price, plot_date, entity, type=2):
        self.price = plot_price
        self.date = plot_date
        if type == 1:
            self.patient_financial = entity
        if type == 2:
            self.cost = entity
        self.type = type
        self.save()

    def get_input_label(self):
        if self.input:
            return '<span class="label label-default">Entrada</span>'
        return '<span class="label label-default">Parcela</span>'

    def get_type(self):
        if self.type==1:
            return 'Entrada'
        elif self.type==2:
            return 'Parcela'
        return 'Custo'

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