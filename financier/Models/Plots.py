from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal

class Plots(models.Model):
    defou = Decimal('0.00')
    plot01 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot02 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot03 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot04 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot05 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot06 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot07 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot08 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot09 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot10 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot11 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    plot12 = models.DecimalField(max_digits=7, decimal_places=2, default=defou)
    date01 = models.DateField(null=True)
    date02 = models.DateField(null=True)
    date03 = models.DateField(null=True)
    date04 = models.DateField(null=True)
    date05 = models.DateField(null=True)
    date06 = models.DateField(null=True)
    date07 = models.DateField(null=True)
    date07 = models.DateField(null=True)
    date08 = models.DateField(null=True)
    date09 = models.DateField(null=True)
    date10 = models.DateField(null=True)
    date11 = models.DateField(null=True)
    date12 = models.DateField(null=True)
    
    #@classmethod
    def created(self, amount, amount_paid, numPlots, payday=None):
        if payday == None:
            payday = datetime.today()
        amount -= amount_paid
        currentDate = datetime.today()
        valPlot = round(amount / numPlots, 2)
        remainder = amount - (valPlot * numPlots)
        if remainder < amount:
            remainder *= -1
        contPlots = 1
        while contPlots <= numPlots:
            if contPlots == 1:
                self.plot01 = valPlot + remainder
                self.date01 = payday
                currentDate = payday
            elif contPlots == 2:
                self.plot02 = valPlot
                self.date02 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 3:
                self.plot03 = valPlot
                self.date03 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 4:
                self.plot04 = valPlot
                self.date04 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 5:
                self.plot05 = valPlot
                self.date05 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 6:
                self.plot06 = valPlot
                self.date06 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 7:
                self.plot07 = valPlot
                self.date07 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 8:
                self.plot08 = valPlot
                self.date08 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 9:
                self.plot09 = valPlot
                self.date09 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 10:
                self.plot10 = valPlot
                self.date10 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 11:
                self.plot11 = valPlot
                self.date11 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            elif contPlots == 12:
                self.plot12 = valPlot
                self.date12 = currentDate + timedelta(days=30)
                currentDate = currentDate + timedelta(days=30)
            contPlots += 1
    
    def format_date(self, date00):
        if date00 != None:
            return date00.strftime("%d/%m/%Y")
        return ' --/--/---- '

    def __str__(self):
        return( str(self.plot01)+' - '+self.format_date(self.date01)+'\n'+ str(self.plot02)+' - '+self.format_date(self.date02)+'\n'+
                str(self.plot03)+' - '+self.format_date(self.date03)+'\n'+ str(self.plot04)+' - '+self.format_date(self.date04)+'\n'+
                str(self.plot05)+' - '+self.format_date(self.date05)+'\n'+ str(self.plot06)+' - '+self.format_date(self.date06)+'\n'+
                str(self.plot07)+' - '+self.format_date(self.date07)+'\n'+ str(self.plot08)+' - '+self.format_date(self.date08)+'\n'+
                str(self.plot09)+' - '+self.format_date(self.date09)+'\n'+ str(self.plot10)+' - '+self.format_date(self.date10)+'\n'+
                str(self.plot11)+' - '+self.format_date(self.date11)+'\n'+ str(self.plot12)+' - '+self.format_date(self.date12)+'\n')

    def get_plot(self, num):
        if num == 1:
            return[self.plot01, self.date01]
        elif num == 2:
            return[self.plot02, self.date02]
        elif num == 3:
            return[self.plot03, self.date03]
        elif num == 4:
            return[self.plot04, self.date04]
        elif num == 5:
            return[self.plot05, self.date05]
        elif num == 6:
            return[self.plot06, self.date06]
        elif num == 7:
            return[self.plot07, self.date07]
        elif num == 8:
            return[self.plot08, self.date08]
        elif num == 9:
            return[self.plot09, self.date09]
        elif num == 10:
            return[self.plot10, self.date10]
        elif num == 11:
            return[self.plot11, self.date11]
        elif num == 12:
            return[self.plot12, self.date12]

    def as_dict(self):
        return {
            'plot01', self.plot01,
            'plot02', self.plot02,
            'plot03', self.plot03,
            'plot04', self.plot04,
            'plot05', self.plot05,
            'plot06', self.plot06,
            'plot07', self.plot07,
            'plot08', self.plot08,
            'plot10', self.plot10,
            'plot11', self.plot11,
            'plot12', self.plot12,
            'date01', self.date01,
            'date02', self.date02,
            'date03', self.date03,
            'date04', self.date04,
            'date05', self.date05,
            'date06', self.date06,
            'date07', self.date07,
            'date08', self.date08,
            'date09', self.date09,
            'date10', self.date10,
            'date11', self.date11,
            'date12', self.date12,
        }
