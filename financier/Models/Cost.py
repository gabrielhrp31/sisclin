from django.db import models


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
    
    def __str__(self):
        return self.description

    def get_cost_type(self):
        return '<span class="label label-primary">Fixo</span>' if self.cost_type else '<span class="label label-primary">Variável</span>'

    def get_payment_form(self):
        return 'À vista' if self.payment_form else 'À prazo'

    def get_payment_status(self):
        pass

    def get_status(self):
        return 'FINALIZADO' if self.status else 'PENDENTE'
        
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
            'status', self.status,
        }
