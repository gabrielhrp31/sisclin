from django.db import models

from datetime import datetime

from financier.Models import Plots


class Cost(models.Model):
    cost_type = models.NullBooleanField(null=False)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_form = models.NullBooleanField(null=False)
    num_plots = models.IntegerField(null=True)
    payday = models.DateField(null=True)
    creation_date = models.DateField(auto_now_add=True)
    change_date = models.DateField(null=False, auto_now=True)
    change_hour = models.TimeField(null=False, auto_now=True)
    status = models.NullBooleanField(null=False)

    def get_cost_type(self):
        return '<span class="label label-primary">Fixo</span>' if self.cost_type else '<span class="label label-primary">Variável</span>'

    def get_payment_form(self):
        return 'À vista' if self.payment_form else 'À prazo'

    def get_payment_date(self):
        plot = Plots.Plots.objects.filter(cost=self.id, paid_day__month=datetime.now().month)
        return plot[0].paid_day if plot else None

    def as_plot(self):
        plot = Plots.Plots()
        plot.cost = self
        plot.price = self.amount
        plot.date = self.payday
        plot.input = False
        plot.paid_day = self.get_payment_date()
        plot.type = 3
        return plot

    def as_dict(self):
        return {
            'cost_type', self.cost_type,
            'description', self.description,
            'amount', self.amount,
            'payment_form', self.payment_form,
            'num_plots', self.num_plots,
            'payday', self.payday,
            'creation_date', self.creation_date,
            'change_date', self.change_date,
            'change_hour', self.change_hour,
        }
