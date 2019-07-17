from django.db import models

from datetime import datetime, date, timedelta

from financier.Models import Plots


class Cost(models.Model):
    cost_type = models.NullBooleanField(null=False)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
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

    def get_payment_date(self, year, month):
        if year and month:
            return self.payday - (date.today().replace(day=1)-self.payday.replace(day=1, year=year, month=month))
        return self.payday - (date.today().replace(day=1)-self.payday.replace(day=1, year=datetime.now().year, month=datetime.now().month))

    def get_paid_day(self, year=None, month=None):
        if year and month:
            plot = Plots.Plots.objects.filter(cost=self.id, paid_day__month=month, paid_day__year=year)
        else:
            plot = Plots.Plots.objects.filter(cost=self.id, paid_day__month=datetime.now().month, paid_day__year=datetime.now().year)
        return plot[0].paid_day if plot else None

    def get_payment_status(self, month, year):
        plot = None
        if year and month:
            plot = Plots.Plots.objects.filter(cost=self.id, paid_day__isnull=False, date__month=month, date__year=year)
            print(plot)
        if plot:
            return True
        return False

    def as_plot(self, year=None, month=None):
        plot = Plots.Plots()
        plot.cost = self
        plot.price = self.amount
        plot.date = self.get_payment_date(year, month)
        plot.input = False
        plot.paid_day = self.get_paid_day(year, month)
        plot.type = 3
        plot.status = self.get_payment_status(year, month)
        # print(plot.paid_day)
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
