from datetime import datetime

from django.db import models

from patients.Models.Patient import Patient


def get_full_date(date, time):
    str = date.strftime("%d/%m/%Y")+" "+time.strftime("%H:%M:%S")
    full_date = datetime.strptime(str, "%d/%m/%Y %H:%M:%S")
    print(full_date)
    return full_date


class Consultation(models.Model):
    title = models.TextField(null=False)
    start = models.DateField(null=False)
    startTime = models.TimeField(null=True)
    end = models.DateField(null=False)
    endTime = models.TimeField(null=True)
    description = models.TextField(null=True)
    payment = models.BooleanField(null=False, default=False)
    allDay = models.BooleanField(default=False)
    holiday = models.BooleanField(default=False)
    backgroundColor = models.CharField(max_length=7, default="#000000")
    textColor = models.CharField(max_length=7, default="#ffffff")
    patient = models.ForeignKey(Patient,null=True,default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_rendering(self):
        if self.holiday:
            return 'background'
        else:
            return ''

    def as_dict(self):
        return {
            'id': self.id,
            'allDay': self.allDay,
            'start': get_full_date(self.start , self.startTime),
            'end': get_full_date(self.end,self.endTime),
            'title': self.title,
            'backgroundColor': self.backgroundColor,
            'textColor': self.textColor,
            'patient': self.patient.id,
            'borderColor': '#ffffff',
            'rendering': self.get_rendering()
        }
